"""Tests contra fuga de información (secciones 16 y 27.4).

Los tests de escalado y codificación dentro del pipeline se agregan con los
modelos de la Fase 5; acá se verifica la mecánica de validación que todos usan.
"""

import numpy as np
import pandas as pd

from src.models.validation import (
    add_high_mortality_label,
    cross_validate_classification,
    cross_validate_regression,
    evaluation_set,
    loyo_folds,
)


def test_funcion_de_prediccion_nunca_ve_el_anio_de_prueba(panel):
    data = evaluation_set(panel, with_lag=False)
    seen = []

    def spy(train, test):
        test_years = set(test["AnioEjercicio"])
        assert len(test_years) == 1
        assert not test_years & set(train["AnioEjercicio"])
        seen.append(test_years.pop())
        return np.zeros(len(test))

    oof = cross_validate_regression(data, spy, "intensidad_ug_ha", "espia")
    assert sorted(seen) == sorted(data["AnioEjercicio"].unique())
    assert (oof["fold"] == oof["AnioEjercicio"]).all()


def test_umbral_no_depende_del_anio_de_prueba(panel):
    data = evaluation_set(panel, with_lag=False)
    fold = next(loyo_folds(data))
    _, _, thresholds = add_high_mortality_label(fold.train, fold.test, 0.75)
    altered = fold.test.assign(tasa_mortalidad_1000=fold.test["tasa_mortalidad_1000"] * 100)
    _, labelled, thresholds_altered = add_high_mortality_label(fold.train, altered, 0.75)
    pd.testing.assert_series_equal(thresholds, thresholds_altered)
    assert (labelled["mortalidad_elevada"] == 1).all()


def test_umbral_se_recalcula_en_cada_fold(panel):
    data = evaluation_set(panel, with_lag=False)

    def constant(train, test):
        return np.zeros(len(test)), np.zeros(len(test), dtype=int)

    oof = cross_validate_classification(data, constant, "constante", 0.75)
    per_fold = oof.groupby(["DepartamentoCodigo", "fold"])["umbral_mortalidad_elevada"].first()
    assert (per_fold.groupby("DepartamentoCodigo").nunique() > 1).all()


def test_etiqueta_no_esta_en_los_datos_de_entrada(panel):
    data = evaluation_set(panel, with_lag=False)
    assert "mortalidad_elevada" not in data.columns


def test_predicciones_reportadas_son_fuera_de_muestra(panel):
    """Un modelo que memoriza el entrenamiento no puede acertar en la prueba."""
    data = evaluation_set(panel, with_lag=False)

    def memorizer(train, test):
        lookup = train.set_index(["DepartamentoCodigo", "AnioEjercicio"])["intensidad_ug_ha"]
        keys = list(zip(test["DepartamentoCodigo"], test["AnioEjercicio"]))
        return np.array([lookup.get(k, np.nan) for k in keys])

    oof = cross_validate_regression(data, memorizer, "intensidad_ug_ha", "memoria")
    assert oof["y_pred"].isna().all()
