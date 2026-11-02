"""Tests del Chill Index (secciones 11.5 y 27.3)."""

import math

import numpy as np
import pandas as pd
import pytest

from src.features.chill_index import chill_category, chill_index, rain_term, wind_speed_ms


def test_conversion_viento_86_4_km_dia_es_1_ms():
    assert wind_speed_ms(86.4) == pytest.approx(1.0, abs=1e-12)


def test_valor_conocido_sin_lluvia():
    # (11,7 + 3,1 × √1) × (40 − 10) + 481 + 0 = 14,8 × 30 + 481 = 925
    assert chill_index(10.0, 1.0, 0.0) == pytest.approx(925.0)


def test_valor_conocido_con_lluvia():
    expected = 925.0 + 418 * (1 - math.exp(-0.4))
    assert chill_index(10.0, 1.0, 10.0) == pytest.approx(expected)


def test_termino_de_lluvia_cero_sin_precipitacion():
    assert rain_term(0.0) == 0.0


def test_mas_viento_aumenta_ci():
    assert chill_index(10.0, 4.0, 5.0) > chill_index(10.0, 1.0, 5.0)


def test_menos_temperatura_aumenta_ci():
    assert chill_index(5.0, 2.0, 5.0) > chill_index(15.0, 2.0, 5.0)


def test_mas_lluvia_aumenta_ci():
    assert chill_index(10.0, 2.0, 20.0) > chill_index(10.0, 2.0, 5.0)


@pytest.mark.parametrize("args", [(np.nan, 1.0, 0.0), (10.0, np.nan, 0.0), (10.0, 1.0, np.nan)])
def test_faltante_si_falta_cualquier_entrada(args):
    assert np.isnan(chill_index(*args))


def test_vectorizado_conserva_faltantes():
    ci = chill_index(pd.Series([10.0, 10.0]), pd.Series([1.0, np.nan]), pd.Series([0.0, 0.0]))
    assert ci.iloc[0] == pytest.approx(925.0)
    assert pd.isna(ci.iloc[1])


@pytest.mark.parametrize(
    "value, label",
    [
        (899.999, "Sin riesgo"),
        (900, "Riesgo bajo"),
        (999.999, "Riesgo bajo"),
        (1000, "Riesgo medio"),
        (1100, "Riesgo alto"),
        (1199.999, "Riesgo alto"),
        (1200, "Condiciones críticas"),
        (1500, "Condiciones críticas"),
    ],
)
def test_categorias_en_los_limites(value, label):
    assert chill_category(pd.Series([value])).iloc[0] == label


def test_categoria_faltante():
    assert pd.isna(chill_category(pd.Series([np.nan])).iloc[0])
