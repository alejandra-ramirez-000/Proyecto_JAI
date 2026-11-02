"""Tests de datos crudos (sección 27.1) y de las funciones de carga."""

import unicodedata

import pandas as pd
import pytest

from src.config import project_path
from src.data.audit import check_raw_hashes, climate_coverage
from src.data.load_inia import STATION_COLUMN, load_inia, select_stations
from src.data.load_snig import (
    DIMENSION_COLUMNS,
    MGAP_COLUMNS,
    filter_generales,
    filter_ovinos,
    load_catalogo,
    parse_decimal_comma,
    select_ovinos,
)

# ---------------------------------------------------------------------------
# SNIG
# ---------------------------------------------------------------------------


def test_anios_snig(animales, generales, cfg):
    first, last = cfg["project"]["snig_years"]
    expected = list(range(first, last + 1))
    assert sorted(animales["Anio"].unique()) == expected
    assert sorted(generales["Anio"].unique()) == expected


def test_cantidad_de_filas(animales, generales, cfg):
    assert len(animales) == cfg["expected_raw"]["animales_rows"]
    assert len(generales) == cfg["expected_raw"]["generales_rows"]


def test_departamentos_esperados_existen(animales, generales, cfg):
    for df in (animales, generales):
        assert set(cfg["departments"]) <= set(df["DepartamentoCodigo"])


def test_especie_2_es_ovinos(cfg):
    especies = load_catalogo(project_path(cfg["paths"]["catalogo_especies"]))
    descripcion = especies.set_index("EspecieCodigo")["EspecieDescripcion"]
    assert descripcion[cfg["species"]["sheep_code"]] == "OVINOS"


def test_ovinos_en_alcance(animales, cfg):
    ovinos = select_ovinos(animales, cfg)
    assert len(ovinos) == cfg["expected_raw"]["ovinos_rows_scope"]
    assert ovinos.groupby(["DepartamentoCodigo", "Anio"]).ngroups == cfg["expected_raw"]["department_years_scope"]


def test_modelable_sin_negativos_ni_faltantes(animales, generales, cfg):
    start, end = cfg["project"]["start_year"], cfg["project"]["end_year"]
    ovinos = filter_ovinos(animales, cfg)
    gen = filter_generales(generales, cfg)
    for df in (ovinos, gen):
        assert df["Anio"].between(start, end).all()
        assert set(df["DepartamentoCodigo"]) == set(cfg["departments"])
    assert (ovinos[["AnimalesPorEspecieMortandadPD_AD", "AnimalesPorEspeciePD_AD"]] >= 0).all().all()
    assert (gen[["UnidadesGanaderas", "SuperficieGanadera"]] >= 0).all().all()
    assert (ovinos["EspecieCodigo"] == cfg["species"]["sheep_code"]).all()


def test_clave_dimensional_sin_duplicados(animales, generales):
    assert not animales.duplicated(DIMENSION_COLUMNS + ["EspecieCodigo"] + MGAP_COLUMNS).any()
    assert not generales.duplicated(DIMENSION_COLUMNS + MGAP_COLUMNS).any()


def test_columnas_mgap_vacias_hasta_2021(animales, generales):
    for df in (animales, generales):
        nulls = df[MGAP_COLUMNS].isna().all(axis=1).groupby(df["Anio"]).mean()
        assert (nulls.loc[:2021] == 1).all()
        assert (nulls.loc[2022:] == 0).all()


def test_codigos_conservan_ceros_a_la_izquierda(animales):
    assert "01" in set(animales["GiroCodigo"])


def test_parse_decimal_comma():
    parsed = parse_decimal_comma(pd.Series(["19,64", "0,00", "********", "1200"]))
    assert parsed.iloc[0] == pytest.approx(19.64)
    assert parsed.iloc[1] == 0
    assert pd.isna(parsed.iloc[2])
    assert parsed.iloc[3] == 1200
    with pytest.raises(ValueError):
        parse_decimal_comma(pd.Series(["abc"]))


def _generales_sinteticas(superficie_ganadera):
    return pd.DataFrame(
        {
            "Anio": [2020] * len(superficie_ganadera),
            "DepartamentoCodigo": [2] * len(superficie_ganadera),
            "UnidadesGanaderas": [1.0] * len(superficie_ganadera),
            "SuperficieGanadera": superficie_ganadera,
        }
    )


def test_filter_generales_rechaza_negativos(cfg):
    with pytest.raises(ValueError, match="negativos"):
        filter_generales(_generales_sinteticas([10.0, -1.0]), cfg)


def test_filter_generales_rechaza_enmascarados(cfg):
    with pytest.raises(ValueError, match="faltantes"):
        filter_generales(_generales_sinteticas([10.0, float("nan")]), cfg)


def test_filter_generales_ignora_negativos_fuera_del_periodo(cfg):
    df = _generales_sinteticas([10.0, -1.0])
    df.loc[1, "Anio"] = 2016
    assert len(filter_generales(df, cfg)) == 1


def test_filter_ovinos_rechaza_mortalidad_negativa(cfg):
    df = pd.DataFrame(
        {
            "Anio": [2020],
            "DepartamentoCodigo": [2],
            "EspecieCodigo": [cfg["species"]["sheep_code"]],
            "AnimalesPorEspecieMortandadPD_AD": [-1],
            "AnimalesPorEspeciePD_AD": [100],
        }
    )
    with pytest.raises(ValueError, match="negativos"):
        filter_ovinos(df, cfg)


def test_raw_sin_modificaciones(cfg):
    hashes = check_raw_hashes(cfg)
    assert hashes["sha256_registrado"].notna().all(), "falta registrar hashes: python -m src.data.audit --registrar-hashes"
    assert hashes["coincide"].all(), hashes[~hashes["coincide"]]["archivo"].tolist()


def test_no_se_lee_carpeta_no_usar(cfg):
    assert not any("No usar" in str(path) for path in cfg["paths"].values())


# ---------------------------------------------------------------------------
# INIA
# ---------------------------------------------------------------------------


def test_inia_fechas_validas_y_unicas(inia, cfg):
    assert inia["Fecha"].notna().all()
    assert not inia.duplicated([STATION_COLUMN, "Fecha"]).any()
    assert str(inia["Fecha"].min().date()) == cfg["expected_raw"]["inia_first_date"]
    assert str(inia["Fecha"].max().date()) == cfg["expected_raw"]["inia_last_date"]


def test_inia_nombres_en_nfc(inia):
    assert all(unicodedata.is_normalized("NFC", s) for s in inia[STATION_COLUMN].unique())


def test_select_stations_asigna_cinco_departamentos(inia, cfg):
    selected = select_stations(inia, cfg)
    assert set(selected["DepartamentoCodigo"]) == set(cfg["departments"])
    assert selected.groupby("DepartamentoCodigo")[STATION_COLUMN].nunique().eq(1).all()
    assert not selected[STATION_COLUMN].str.contains("Glencore").any()
    tacuarembo = selected.loc[selected["DepartamentoCodigo"] == 18, STATION_COLUMN].unique()
    assert list(tacuarembo) == ["Tacuarembó La Magnolia"]


def test_select_stations_falla_si_falta_una_estacion(inia, cfg):
    with pytest.raises(ValueError, match="faltan estaciones"):
        select_stations(inia[inia[STATION_COLUMN] != "Salto Grande"], cfg)


def test_select_stations_falla_con_estacion_desconocida(inia, cfg):
    extra = inia.head(1).assign(**{STATION_COLUMN: "Estación Nueva"})
    with pytest.raises(ValueError, match="no previstas"):
        select_stations(pd.concat([inia, extra]), cfg)


def _write_inia(tmp_path, rows):
    df = pd.DataFrame(
        rows, columns=["Anio", "Mes", "Dia", "EstacionAgr", "TempAireMedia", "PrecipAcum", "RecorridoViento"]
    )
    path = tmp_path / "inia.csv"
    df.to_csv(path, index=False)
    return path


def test_load_inia_rechaza_fecha_imposible(tmp_path):
    path = _write_inia(tmp_path, [[2021, 2, 30, "Las Brujas", 10.0, 0.0, 100.0]])
    with pytest.raises(ValueError, match="fecha imposible"):
        load_inia(path)


def test_load_inia_rechaza_duplicados(tmp_path):
    row = [2021, 2, 1, "Las Brujas", 10.0, 0.0, 100.0]
    with pytest.raises(ValueError, match="duplicados"):
        load_inia(_write_inia(tmp_path, [row, row]))


def test_load_inia_normaliza_nfd(tmp_path):
    nfd = unicodedata.normalize("NFD", "Tacuarembó La Magnolia")
    df = load_inia(_write_inia(tmp_path, [[2021, 2, 1, nfd, 10.0, 0.0, 100.0]]))
    assert df[STATION_COLUMN].iloc[0] == "Tacuarembó La Magnolia"


def test_cobertura_climatica_minima_en_periodo(inia, cfg):
    start, end = cfg["project"]["start_year"], cfg["project"]["end_year"]
    coverage = climate_coverage(select_stations(inia, cfg), cfg)
    in_period = coverage[coverage["AnioEjercicio"].between(start, end)]
    assert len(in_period) == cfg["expected_panel"]["rows"]
    assert in_period["cumple_minimo"].all()
