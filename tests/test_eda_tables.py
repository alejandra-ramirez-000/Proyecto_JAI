"""Tests de las tablas del análisis exploratorio."""

import numpy as np
import pandas as pd
import pytest

from src.reporting import tables as tab


def test_desvio_intra_departamento_tiene_media_cero(panel):
    demeaned = tab.within_department(panel, list(tab.TARGETS))
    means = demeaned.groupby(panel["DepartamentoCodigo"]).mean()
    assert np.allclose(means.values, 0)


def test_correlacion_intra_coincide_con_calculo_manual(panel):
    correlations = tab.correlation_table(panel)
    row = correlations[
        (correlations["objetivo"] == "tasa_mortalidad_1000") & (correlations["columna"] == "dias_ci_ge_1000_ejercicio")
    ].iloc[0]
    x = panel["dias_ci_ge_1000_ejercicio"] - panel.groupby("DepartamentoCodigo")["dias_ci_ge_1000_ejercicio"].transform("mean")
    y = panel["tasa_mortalidad_1000"] - panel.groupby("DepartamentoCodigo")["tasa_mortalidad_1000"].transform("mean")
    assert row["r_intra_departamento"] == pytest.approx(np.corrcoef(x, y)[0, 1])
    assert row["r_global"] == pytest.approx(np.corrcoef(panel["dias_ci_ge_1000_ejercicio"], panel["tasa_mortalidad_1000"])[0, 1])
    assert row["n"] == 45


def test_doble_diferencia_tiene_media_cero_por_departamento_y_anio(panel):
    two_way = tab.within_department_and_year(panel, list(tab.TARGETS))
    assert np.allclose(two_way.groupby(panel["DepartamentoCodigo"]).mean().values, 0)
    assert np.allclose(two_way.groupby(panel["AnioEjercicio"]).mean().values, 0)


def test_correlacion_de_rezagos_usa_40_observaciones(panel):
    correlations = tab.correlation_table(panel)
    assert (correlations.loc[correlations["ventana"] == "historia", "n"] == 40).all()


def test_correlacion_sin_variacion_es_faltante():
    r, n = tab._pearson(pd.Series([1.0, 1.0, 1.0]), pd.Series([1.0, 2.0, 3.0]))
    assert np.isnan(r) and n == 3


def test_anios_extremos_respetan_umbral(panel):
    extremes = tab.extreme_years(panel, threshold=1.5)
    z_cols = [c for c in extremes.columns if c.startswith("z_")]
    assert (extremes[z_cols].abs() >= 1.5).any(axis=1).all()
    assert len(tab.extreme_years(panel, threshold=10)) == 0


def test_dias_por_categoria_suman_dias_validos(panel_tables, cfg):
    daily = panel_tables["clima_diario_con_ci"]
    years = (cfg["project"]["start_year"], cfg["project"]["end_year"])
    counts = tab.ci_category_days(daily, years)
    totals = counts.groupby(["DepartamentoCodigo", "AnioEjercicio"])["dias"].sum()
    panel = panel_tables["panel"].set_index(["DepartamentoCodigo", "AnioEjercicio"])
    assert (totals == panel.loc[totals.index, "dias_validos_ejercicio"]).all()


def test_comparacion_de_ventanas_tiene_ambas(panel):
    comparison = tab.window_comparison(tab.correlation_table(panel))
    assert {"ejercicio", "jul_oct"} <= set(comparison.columns)
    assert len(comparison) == len(tab.TARGETS) * len(tab.CLIMATE_VARIABLES)
