"""Tests de folds, métricas, bootstrap y baselines."""

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import balanced_accuracy_score, roc_auc_score

from src.models import baselines as bl
from src.models.validation import (
    LABEL,
    add_high_mortality_label,
    balanced_accuracy_stat,
    classification_metrics,
    cross_validate_classification,
    cross_validate_regression,
    evaluation_set,
    inner_year_splits,
    loyo_folds,
    mae_skill,
    mae_stat,
    regression_metrics,
    roc_auc_stat,
    year_block_bootstrap,
)


@pytest.fixture(scope="module")
def full(panel):
    return evaluation_set(panel, with_lag=False)


@pytest.fixture(scope="module")
def lagged(panel):
    return evaluation_set(panel, with_lag=True)


# ---------------------------------------------------------------------------
# Folds
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("with_lag, n_rows, n_folds", [(False, 45, 9), (True, 40, 8)])
def test_conjuntos_de_evaluacion(panel, with_lag, n_rows, n_folds):
    data = evaluation_set(panel, with_lag)
    folds = list(loyo_folds(data))
    assert len(data) == n_rows
    assert len(folds) == n_folds
    for fold in folds:
        assert len(fold.test) == 5
        assert set(fold.test["AnioEjercicio"]) == {fold.year}
        assert fold.year not in set(fold.train["AnioEjercicio"])
        assert fold.test["DepartamentoCodigo"].nunique() == 5
    tested = pd.concat([f.test for f in folds])
    assert len(tested) == n_rows and not tested.duplicated(["DepartamentoCodigo", "AnioEjercicio"]).any()


def test_validacion_interna_por_anio(full):
    fold = next(loyo_folds(full))
    splits = inner_year_splits(fold.train)
    assert len(splits) == fold.train["AnioEjercicio"].nunique()
    years = fold.train["AnioEjercicio"].to_numpy()
    for train_idx, val_idx in splits:
        assert len(set(years[val_idx])) == 1
        assert not set(years[val_idx]) & set(years[train_idx])
        assert fold.year not in set(years)


# ---------------------------------------------------------------------------
# Etiqueta de mortalidad elevada
# ---------------------------------------------------------------------------


def test_umbral_es_percentil_75_del_entrenamiento(full):
    fold = next(loyo_folds(full))
    train, test, thresholds = add_high_mortality_label(fold.train, fold.test, 0.75)
    for code, group in fold.train.groupby("DepartamentoCodigo"):
        assert thresholds[code] == pytest.approx(group["tasa_mortalidad_1000"].quantile(0.75))
    expected = (test["tasa_mortalidad_1000"] > test["DepartamentoCodigo"].map(thresholds)).astype(int)
    assert (test[LABEL] == expected).all()


def test_etiqueta_usa_mayor_estricto():
    train = pd.DataFrame({"DepartamentoCodigo": [2] * 4, "tasa_mortalidad_1000": [10.0, 10.0, 10.0, 10.0],
                          "mortalidad_lag1": [np.nan] * 4})
    test = pd.DataFrame({"DepartamentoCodigo": [2], "tasa_mortalidad_1000": [10.0], "mortalidad_lag1": [11.0]})
    _, labelled, _ = add_high_mortality_label(train, test, 0.75)
    assert labelled[LABEL].iloc[0] == 0
    assert labelled["mortalidad_lag1_elevada"].iloc[0] == 1


# ---------------------------------------------------------------------------
# Métricas
# ---------------------------------------------------------------------------


def test_metricas_de_regresion():
    oof = pd.DataFrame({"y_true": [1.0, 2.0, 3.0], "y_pred": [1.5, 2.0, 2.0]})
    metrics = regression_metrics(oof)
    assert metrics["MAE"] == pytest.approx(0.5)
    assert metrics["RMSE"] == pytest.approx(np.sqrt((0.25 + 0 + 1) / 3))


def test_skill():
    assert mae_skill(0.02, 0.025) == pytest.approx(0.2)
    assert mae_skill(0.03, 0.025) < 0


def test_metricas_de_clasificacion():
    oof = pd.DataFrame({"y_true": [0, 0, 1, 1], "y_proba": [0.1, 0.6, 0.4, 0.9], "y_pred": [0, 1, 0, 1]})
    metrics = classification_metrics(oof)
    assert metrics["balanced_accuracy"] == pytest.approx(0.5)
    assert metrics["roc_auc"] == pytest.approx(0.75)
    assert (metrics["tn"], metrics["fp"], metrics["fn"], metrics["tp"]) == (1, 1, 1, 1)


def test_auc_faltante_con_una_sola_clase():
    oof = pd.DataFrame({"y_true": [0, 0], "y_proba": [0.1, 0.2], "y_pred": [0, 0]})
    assert np.isnan(classification_metrics(oof)["roc_auc"])


def test_estadisticos_rapidos_coinciden_con_sklearn():
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, 60)
    proba = np.round(rng.random(60), 1)  # con empates
    pred = (proba > 0.5).astype(int)
    d = {"y_true": y, "y_proba": proba, "y_pred": pred}
    assert roc_auc_stat(d) == pytest.approx(roc_auc_score(y, proba))
    assert balanced_accuracy_stat(d) == pytest.approx(balanced_accuracy_score(y, pred))
    assert mae_stat({"y_true": np.array([1.0, 3.0]), "y_pred": np.array([2.0, 2.0])}) == 1.0


def test_bootstrap_remuestrea_anios_completos():
    oof = pd.DataFrame({"AnioEjercicio": np.repeat([2018, 2019, 2020], 5), "y_true": np.arange(15.0),
                        "y_pred": np.zeros(15)})
    sizes = []

    def statistic(d):
        sizes.append(len(d["y_true"]))
        return mae_stat(d)

    result = year_block_bootstrap(oof, statistic, ["y_true", "y_pred"], n_boot=50, seed=1)
    assert set(sizes) == {15}
    assert result["ic95_inf"] <= mae_stat({"y_true": oof["y_true"].to_numpy(), "y_pred": np.zeros(15)}) <= result["ic95_sup"]


# ---------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------


def test_r1_promedio_departamental(full):
    oof = cross_validate_regression(full, bl.department_mean("intensidad_ug_ha"), "intensidad_ug_ha", "R1")
    row = oof[(oof["AnioEjercicio"] == 2020) & (oof["DepartamentoCodigo"] == 2)].iloc[0]
    others = full[(full["DepartamentoCodigo"] == 2) & (full["AnioEjercicio"] != 2020)]
    assert row["y_pred"] == pytest.approx(others["intensidad_ug_ha"].mean())


def test_r2_persistencia_es_el_rezago(lagged):
    oof = cross_validate_regression(lagged, bl.persistence("intensidad_lag1"), "intensidad_ug_ha", "R2")
    merged = oof.merge(lagged, on=["DepartamentoCodigo", "AnioEjercicio"])
    assert np.allclose(merged["y_pred"], merged["intensidad_lag1"])


def test_c1_clase_mayoritaria(full):
    oof = cross_validate_classification(full, bl.majority_class, "C1", 0.75)
    assert (oof["y_pred"] == 0).all()
    assert np.allclose(oof["y_proba"], oof["prevalencia_entrenamiento"])


def test_c2_persistencia_de_riesgo(lagged):
    oof = cross_validate_classification(lagged, bl.risk_persistence, "C2", 0.75)
    merged = oof.merge(lagged, on=["DepartamentoCodigo", "AnioEjercicio"])
    expected = (merged["mortalidad_lag1"] > merged["umbral_mortalidad_elevada"]).astype(int)
    assert (merged["y_pred"] == expected).all()


def test_c3_historial_departamental(full):
    fold = next(loyo_folds(full))
    train, test, _ = add_high_mortality_label(fold.train, fold.test, 0.75)
    proba, _ = bl.department_history(train, test)
    expected = test["DepartamentoCodigo"].map(train.groupby("DepartamentoCodigo")[LABEL].mean())
    assert np.allclose(proba, expected)
