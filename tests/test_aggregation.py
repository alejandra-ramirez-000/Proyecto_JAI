"""Tests de agregación climática y de SNIG con datos sintéticos."""

import numpy as np
import pandas as pd
import pytest

from src.data.build_panel import aggregate_animales, aggregate_generales
from src.features.build_features import aggregate_window, daily_climate, expected_days, max_consecutive_days


def _daily(cfg, temps, winds=None, precip=None, start="2019-07-01"):
    n = len(temps)
    inia = pd.DataFrame(
        {
            "EstacionAgr": "Las Brujas",
            "DepartamentoCodigo": 2,
            "Fecha": pd.date_range(start, periods=n),
            "TempAireMedia": temps,
            "PrecipAcum": precip if precip is not None else [0.0] * n,
            "RecorridoViento": winds if winds is not None else [86.4] * n,
        }
    )
    return daily_climate(inia, cfg)


def test_dias_esperados():
    assert expected_days(2020, 7) == 366  # incluye 29/02/2020
    assert expected_days(2021, 7) == 365
    assert expected_days(2021, 7, [7, 8, 9, 10]) == 123


def test_racha_maxima_cortada_por_dia_falso_y_por_hueco():
    dates = pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-05", "2020-01-06"])
    assert max_consecutive_days(pd.Series([True, True, True, True, True]), dates) == 3
    assert max_consecutive_days(pd.Series([True, False, True, True, True]), dates) == 2
    assert max_consecutive_days(pd.Series([False] * 5), dates) == 0


def test_agregado_climatico(cfg):
    # Con viento 1 m/s y sin lluvia: CI = 14,8 × (40 − T) + 481.
    # T = 10 → 925; T = 0 → 1073; T = −10 → 1221.
    temps = [10.0, 0.0, 0.0, -10.0, -10.0, 10.0]
    daily = _daily(cfg, temps)
    out = aggregate_window(daily, cfg, "w").iloc[0]
    assert out["AnioEjercicio"] == 2020
    assert out["dias_validos_w"] == 6
    assert out["dias_esperados_w"] == 366
    assert out["dias_ci_ge_900_w"] == 6
    assert out["dias_ci_ge_1000_w"] == 4
    assert out["dias_ci_ge_1200_w"] == 2
    assert out["racha_max_ci_ge_1000_w"] == 4
    assert out["racha_max_ci_ge_1200_w"] == 2
    assert out["prop_ci_ge_1200_w"] == pytest.approx(2 / 6)
    assert out["ci_max_w"] == pytest.approx(1221.0)
    assert out["temp_media_c_w"] == pytest.approx(np.mean(temps))
    assert out["viento_medio_ms_w"] == pytest.approx(1.0)


def test_dia_incompleto_se_excluye_y_no_se_rellena(cfg):
    daily = _daily(cfg, [-10.0, -10.0, -10.0], winds=[86.4, np.nan, 86.4], precip=[1.0, 50.0, 1.0])
    assert daily["chill_index"].isna().sum() == 1
    out = aggregate_window(daily, cfg, "w").iloc[0]
    assert out["dias_validos_w"] == 2
    assert out["precip_total_mm_w"] == pytest.approx(2.0)
    # El faltante corta la racha: dos días sueltos.
    assert out["racha_max_ci_ge_1200_w"] == 1


def test_ventana_julio_octubre(cfg):
    daily = _daily(cfg, [10.0] * 366)
    out = aggregate_window(daily, cfg, "jo", cfg["climate"]["sensitive_months"]).iloc[0]
    assert out["dias_esperados_jo"] == 123
    assert out["dias_validos_jo"] == 123


def test_intensidad_es_cociente_de_totales():
    generales = pd.DataFrame(
        {
            "Anio": [2020, 2020],
            "DepartamentoCodigo": [2, 2],
            "UnidadesGanaderas": [1.0, 90.0],
            "SuperficieGanadera": [10.0, 100.0],
            "Superficie": [10, 100],
            "CantidadTenedores": [1, 1],
        }
    )
    out = aggregate_generales(generales).iloc[0]
    assert out["intensidad_ug_ha"] == pytest.approx(91 / 110)
    assert out["intensidad_ug_ha"] != pytest.approx((0.1 + 0.9) / 2)


def test_intensidad_faltante_si_superficie_cero():
    generales = pd.DataFrame(
        {
            "Anio": [2020],
            "DepartamentoCodigo": [2],
            "UnidadesGanaderas": [5.0],
            "SuperficieGanadera": [0.0],
            "Superficie": [0],
            "CantidadTenedores": [1],
        }
    )
    assert pd.isna(aggregate_generales(generales).iloc[0]["intensidad_ug_ha"])


def test_mortalidad_por_mil_de_totales(cfg):
    ovinos = pd.DataFrame(
        {
            "Anio": [2020, 2020],
            "DepartamentoCodigo": [2, 2],
            "AnimalesPorEspecieMortandadPD_AD": [1, 9],
            "AnimalesPorEspeciePD_AD": [100, 100],
            "CantidadTenedoresPorEspecie": [1, 1],
            "AnimalesPorEspecieNacimientosPD_AD": [0, 0],
            "AnimalesPorEspeciePD_PF": [0, 0],
        }
    )
    out = aggregate_animales(ovinos, cfg).iloc[0]
    assert out["tasa_mortalidad_1000"] == pytest.approx(50.0)
    assert out["muertes_ovinas"] == 10
    assert out["stock_ovino"] == 200
