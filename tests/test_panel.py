"""Tests del panel departamento–ejercicio construido con los datos reales (secciones 14.5 y 27.1)."""

import pandas as pd
import pytest

from src.data.build_panel import LAG_COLUMNS, check_cardinality, panel_dictionary


def test_cardinalidad(panel, cfg):
    exp = cfg["expected_panel"]
    assert len(panel) == exp["rows"]
    assert panel["DepartamentoCodigo"].nunique() == exp["departments"]
    assert panel["AnioEjercicio"].nunique() == exp["exercises"]
    assert not panel.duplicated(["DepartamentoCodigo", "AnioEjercicio"]).any()


def test_panel_con_rezagos(panel, cfg):
    lagged = panel.dropna(subset=list(LAG_COLUMNS.values()))
    assert len(lagged) == cfg["expected_panel"]["rows_with_lag"]
    assert sorted(lagged["AnioEjercicio"].unique()) == list(range(cfg["project"]["start_year"] + 1, cfg["project"]["end_year"] + 1))


def test_periodo_sin_2016(panel, cfg):
    assert panel["AnioEjercicio"].min() == cfg["project"]["start_year"]
    assert panel["AnioEjercicio"].max() == cfg["project"]["end_year"]


def test_cardinalidad_incorrecta_detiene_el_pipeline(panel, cfg):
    with pytest.raises(ValueError, match="Cardinalidad"):
        check_cardinality(panel.iloc[:-1], cfg)
    with pytest.raises(ValueError, match="duplicados"):
        check_cardinality(pd.concat([panel, panel.iloc[[0]]]), cfg)


def test_cobertura_minima(panel, cfg):
    minimum = cfg["climate"]["minimum_coverage"]
    assert (panel["cobertura_ejercicio"] >= minimum).all()
    assert (panel["cobertura_jul_oct"] >= minimum).all()


def test_objetivos_sin_faltantes_y_en_rango(panel):
    # Rangos observados en la auditoría preliminar (sección 12).
    assert panel["intensidad_ug_ha"].notna().all()
    assert panel["tasa_mortalidad_1000"].notna().all()
    assert panel["intensidad_ug_ha"].between(0.6, 1.3).all()
    assert panel["tasa_mortalidad_1000"].between(25, 120).all()


def test_objetivos_reconstruibles_desde_componentes(panel, cfg):
    intensity = panel["unidades_ganaderas"] / panel["superficie_ganadera"]
    mortality = cfg["targets"]["mortality_per"] * panel["muertes_ovinas"] / panel["stock_ovino"]
    assert (intensity - panel["intensidad_ug_ha"]).abs().max() < 1e-12
    assert (mortality - panel["tasa_mortalidad_1000"]).abs().max() < 1e-9


def test_una_estacion_por_departamento(panel):
    assert panel.groupby("DepartamentoCodigo")["EstacionAgr"].nunique().eq(1).all()
    assert panel.loc[panel["DepartamentoCodigo"] == 18, "EstacionAgr"].iloc[0] == "Tacuarembó La Magnolia"


def test_etiqueta_de_mortalidad_elevada_no_esta_en_el_panel(panel):
    # Se calcula dentro de cada fold (sección 12.3); tenerla aquí sería fuga.
    assert not any("elevada" in c.lower() for c in panel.columns)


def test_diccionario_cubre_todas_las_columnas(panel):
    dictionary = panel_dictionary(panel)
    assert list(dictionary["columna"]) == list(panel.columns)
    assert dictionary["descripcion"].str.len().gt(0).all()
