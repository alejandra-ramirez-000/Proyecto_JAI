"""Tests de conjuntos de variables, pipelines, selección de hiperparámetros y criterios (secciones 13.6, 16, 20 y 27.4)."""

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression, Ridge

from src.models import tuning
from src.models.assessment import sign_stability
from src.models.classification import classification_specs
from src.models.feature_sets import CLIMATE_SETS, feature_specs
from src.models.regression import regression_specs
from src.models.tuning import TunedModel, build_pipeline
from src.models.validation import (
    add_high_mortality_label,
    cross_validate_classification,
    cross_validate_regression,
    evaluation_set,
    loyo_folds,
)


@pytest.fixture(scope="module")
def full(panel):
    return evaluation_set(panel, with_lag=False)


@pytest.fixture(scope="module")
def lagged(panel):
    return evaluation_set(panel, with_lag=True)


# ---------------------------------------------------------------------------
# Conjuntos de variables
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("target", ["intensidad_ug_ha", "tasa_mortalidad_1000"])
def test_variables_existen_y_departamento_no_es_numerico(panel, target):
    for spec in feature_specs(target):
        assert set(spec["numeric"]) <= set(panel.columns)
        assert "DepartamentoCodigo" not in spec["numeric"]
        assert len(spec["numeric"]) <= 4  # muestra pequeña: pocas variables


def test_conjuntos_predefinidos():
    assert CLIMATE_SETS["A"] == ["temp_media_c", "precip_total_mm", "viento_medio_ms"]
    assert CLIMATE_SETS["B"] == ["dias_ci_ge_1000", "dias_ci_ge_1200", "ci_max"]
    control = [s for s in feature_specs("intensidad_ug_ha") if s["set"] == "H"]
    assert control == [{"set": "H", "window": "sin_clima", "numeric": ["intensidad_lag1"], "requires_lag": True}]


def test_especificaciones_y_roles():
    reg = regression_specs()
    principal = {s.name for s in reg if s.role == "principal"}
    assert principal == {"ridge_A_ejercicio", "ridge_B_ejercicio", "ridge_C-A_ejercicio", "ridge_C-B_ejercicio"}
    assert {s.name for s in reg if s.role == "control"} == {"ridge_H_sin_clima"}
    cls = classification_specs(0.75)
    assert {s.name for s in cls if s.role == "control"} == {"logistica_H_sin_clima"}
    assert all(s.role == "sensibilidad" for s in cls if s.family == "bosque")


# ---------------------------------------------------------------------------
# Pipelines: escalado y codificación dentro del fold
# ---------------------------------------------------------------------------


def test_escalador_se_ajusta_solo_con_entrenamiento(full):
    fold = next(loyo_folds(full))
    numeric = ["temp_media_c_ejercicio", "precip_total_mm_ejercicio"]
    pipeline = build_pipeline(Ridge(), numeric).fit(fold.train, fold.train["intensidad_ug_ha"])
    scaler = pipeline.named_steps["prep"].named_transformers_["num"]
    assert np.allclose(scaler.mean_, fold.train[numeric].mean())
    assert not np.allclose(scaler.mean_, full[numeric].mean())


def test_departamento_se_codifica_dentro_del_pipeline(full):
    fold = next(loyo_folds(full))
    pipeline = build_pipeline(Ridge(), ["temp_media_c_ejercicio"]).fit(fold.train, fold.train["intensidad_ug_ha"])
    names = pipeline.named_steps["prep"].get_feature_names_out()
    assert sorted(n for n in names if n.startswith("dep__")) == [f"dep__DepartamentoCodigo_{c}" for c in (15, 18, 19, 2, 4)]


# ---------------------------------------------------------------------------
# Selección de hiperparámetros
# ---------------------------------------------------------------------------


class _SpyModel(TunedModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.train_years = []

    def _inner_score(self, train, params):
        self.train_years.append(set(train["AnioEjercicio"]))
        return (0.0, 0.0)


def test_seleccion_no_ve_el_anio_de_prueba(full):
    model = _SpyModel(Ridge(), {"alpha": [100, 1]}, ["temp_media_c_ejercicio"], "regression")
    oof = cross_validate_regression(full, model, "intensidad_ug_ha", "espia")
    assert len(model.records) == 9
    # Dos candidatos por fold: dos llamadas de selección por cada registro, en orden.
    assert len(model.train_years) == 18
    for i, record in enumerate(model.records):
        for years in model.train_years[2 * i: 2 * i + 2]:
            assert len(years) == 8 and record["fold"] not in years
    assert len(oof) == 45


def test_empate_elige_la_opcion_mas_regularizada(full):
    model = _SpyModel(Ridge(), {"alpha": [100, 30, 0.1]}, ["temp_media_c_ejercicio"], "regression")
    fold = next(loyo_folds(full))
    params, _ = model.select(fold.train)
    assert params == {"alpha": 100}


def test_etiqueta_interna_se_recalcula_sin_el_anio_de_validacion(full, monkeypatch):
    calls = []

    def spy(inner, val, quantile):
        calls.append((set(inner["AnioEjercicio"]), set(val["AnioEjercicio"])))
        return add_high_mortality_label(inner, val, quantile)

    monkeypatch.setattr(tuning, "add_high_mortality_label", spy)
    fold = next(loyo_folds(full))
    train, _, _ = add_high_mortality_label(fold.train, fold.test, 0.75)
    model = TunedModel(LogisticRegression(max_iter=1000), {"C": [1.0]}, ["precip_total_mm_ejercicio"], "classification")
    model._inner_score(train, {"C": 1.0})
    assert len(calls) == 8
    for inner_years, val_years in calls:
        assert len(val_years) == 1 and not inner_years & val_years
        assert fold.year not in inner_years | val_years


def test_registra_hiperparametros_y_coeficientes(lagged):
    model = TunedModel(Ridge(), {"alpha": [10, 1]}, ["dias_ci_ge_1000_ejercicio", "intensidad_lag1"], "regression")
    cross_validate_regression(lagged, model, "intensidad_ug_ha", "ridge")
    assert [r["fold"] for r in model.records] == list(range(2018, 2026))
    first = model.records[0]
    assert first["hiperparametros"]["alpha"] in (10, 1)
    assert {"num__dias_ci_ge_1000_ejercicio", "num__intensidad_lag1"} <= set(first["coeficientes"])


def test_clasificacion_devuelve_probabilidades_y_clases(full):
    model = TunedModel(LogisticRegression(max_iter=1000), {"C": [1.0], "class_weight": ["balanced"]},
                       ["precip_total_mm_ejercicio"], "classification")
    oof = cross_validate_classification(full, model, "logistica", 0.75)
    assert oof["y_proba"].between(0, 1).all()
    assert set(oof["y_pred"]) <= {0, 1}
    assert ((oof["y_proba"] >= 0.5).astype(int) == oof["y_pred"]).all()


# ---------------------------------------------------------------------------
# Criterios
# ---------------------------------------------------------------------------


def test_estabilidad_de_signos():
    coefs = pd.DataFrame(
        {
            "modelo": "m", "conjunto": "c", "fold": [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4],
            "variable": ["num__x"] * 4 + ["num__y"] * 4 + ["num__intensidad_lag1"] * 4,
            "valor": [1, 2, 3, -1, -1, -2, -3, -4, 1, -1, 1, -1],
        }
    )
    assert sign_stability(coefs, "m", "c", {"intensidad_lag1"}) == pytest.approx(0.75)
    assert np.isnan(sign_stability(coefs, "otro", "c", set()))


# ---------------------------------------------------------------------------
# Ronda exploratoria y diagnósticos
# ---------------------------------------------------------------------------


def test_ronda_exploratoria_fija_hiperparametros_sin_tocar_las_registradas():
    from src.models.run_exploratory import FIXED_GRIDS, fixed

    originals = regression_specs()
    fixed_specs = fixed(originals)
    assert fixed_specs and all(s.family == "ridge" and s.name.endswith("_fijo") for s in fixed_specs)
    assert all(s.fit_predict.grid == FIXED_GRIDS["ridge"] for s in fixed_specs)
    # Las especificaciones registradas conservan su grilla completa.
    assert next(s for s in originals if s.name == "ridge_A_ejercicio").fit_predict.grid["alpha"] == [100, 30, 10, 3, 1, 0.1]
    cls = fixed(classification_specs(0.75))
    assert {s.family for s in cls} == {"logistica"}


def test_auc_promedio_por_fold_ignora_folds_de_una_clase():
    from src.models.validation import mean_fold_auc

    oof = pd.DataFrame({
        "fold": [1, 1, 1, 1, 2, 2],
        "y_true": [0, 1, 0, 1, 0, 0],
        "y_proba": [0.1, 0.9, 0.2, 0.8, 0.5, 0.6],
    })
    result = mean_fold_auc(oof)
    assert result["folds_con_ambas_clases"] == 1
    assert result["roc_auc_promedio_folds"] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Criterio de selección v1.1 y ejecución en paralelo
# ---------------------------------------------------------------------------


def test_log_loss_balanceada_coincide_con_sklearn():
    from sklearn.metrics import log_loss
    from sklearn.utils.class_weight import compute_sample_weight

    from src.models.validation import balanced_log_loss_stat

    rng = np.random.default_rng(1)
    y = rng.integers(0, 2, 40)
    p = rng.uniform(0.05, 0.95, 40)
    expected = log_loss(y, p, sample_weight=compute_sample_weight("balanced", y))
    assert balanced_log_loss_stat({"y_true": y, "y_proba": p}) == pytest.approx(expected)


def test_log_loss_balanceada_penaliza_modelo_constante():
    from src.models.validation import balanced_log_loss_stat

    y = np.array([0] * 30 + [1] * 10)
    constant = balanced_log_loss_stat({"y_true": y, "y_proba": np.full(40, 0.25)})
    half = balanced_log_loss_stat({"y_true": y, "y_proba": np.full(40, 0.5)})
    informative = balanced_log_loss_stat({"y_true": y, "y_proba": np.where(y == 1, 0.7, 0.3)})
    assert informative < half < constant


def test_seleccion_de_clasificacion_no_queda_en_modelo_constante(lagged):
    """En el fold 2018 el control H elegía C = 0,01 sin ponderar (casi constante) con el criterio v1.0."""
    model = TunedModel(LogisticRegression(max_iter=5000), {"C": [0.01, 0.1, 0.3, 1, 3, 10],
                       "class_weight": [None, "balanced"]}, ["mortalidad_lag1"], "classification")
    fold = next(loyo_folds(lagged))
    assert fold.year == 2018
    train, _, _ = add_high_mortality_label(fold.train, fold.test, 0.75)
    params, score = model.select(train)
    assert params != {"C": 0.01, "class_weight": None}
    assert np.isfinite(score)


def test_ejecucion_en_paralelo_da_lo_mismo_que_en_serie(panel):
    from src.models.baselines import REGRESSION_BASELINES
    from src.models.experiment import ModelSpec, run_regression

    ridge = TunedModel(Ridge(), {"alpha": [10, 1]}, ["temp_media_c_ejercicio"], "regression")
    specs = REGRESSION_BASELINES + [ModelSpec("ridge_prueba", ridge, requires_lag=False)]
    serial, serial_records = run_regression(panel, specs, n_jobs=1)
    parallel, parallel_records = run_regression(panel, specs, n_jobs=2)
    pd.testing.assert_frame_equal(serial, parallel)
    assert [(r["modelo"], r["conjunto"], r["fold"], r["hiperparametros"]) for r in serial_records] == \
           [(r["modelo"], r["conjunto"], r["fold"], r["hiperparametros"]) for r in parallel_records]


def test_todo_estimador_aleatorio_tiene_semilla():
    """Sin semilla (p. ej. solver saga, árboles, bosque) los resultados cambian entre ejecuciones."""
    from src.models import classification, regression

    for family, entry in {**regression.MODELS, **classification.MODELS}.items():
        params = entry[0].get_params()
        if "random_state" in params and family not in ("ridge", "lineal", "elasticnet", "logistica"):
            assert params["random_state"] is not None, family
    assert classification.MODELS["logistica_en"][0].get_params()["random_state"] is not None
