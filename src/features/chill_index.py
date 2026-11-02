"""Chill Index diario según la fórmula publicada por INIA (sección 11).

    R  = 418 × (1 − exp(−0,04 × P))
    CI = (11,7 + 3,1 × √VV) × (40 − Ta) + 481 + R

CI en kJ/m²/h; VV velocidad media del viento a 2 m (m/s); Ta temperatura media
del aire (°C); P precipitación diaria (mm). Si falta cualquier entrada, el CI
del día queda faltante: no se rellena con cero.
"""

import numpy as np
import pandas as pd

WIND_CONVERSION_DIVISOR = 86.4  # 1 km/día = 1000 m / 86400 s

CATEGORY_LABELS = [
    "Sin riesgo",
    "Riesgo bajo",
    "Riesgo medio",
    "Riesgo alto",
    "Condiciones críticas",
]


def wind_speed_ms(wind_run_km_day, divisor: float = WIND_CONVERSION_DIVISOR):
    """Convierte recorrido del viento (km/día) a velocidad media (m/s)."""
    return wind_run_km_day / divisor


def rain_term(precipitation_mm):
    return 418 * (1 - np.exp(-0.04 * precipitation_mm))


def chill_index(mean_air_temperature_c, wind_speed_ms, precipitation_mm):
    """Chill Index en kJ/m²/h. NaN en cualquier entrada produce NaN."""
    return (
        (11.7 + 3.1 * np.sqrt(wind_speed_ms)) * (40 - mean_air_temperature_c)
        + 481
        + rain_term(precipitation_mm)
    )


def chill_category(ci: pd.Series, thresholds=(900, 1000, 1100, 1200)) -> pd.Series:
    """Categoría oficial INIA: cada umbral es el límite inferior inclusivo de la categoría siguiente."""
    bins = [-np.inf, *thresholds, np.inf]
    return pd.cut(ci, bins=bins, labels=CATEGORY_LABELS, right=False)
