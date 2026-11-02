"""Clima diario con Chill Index y agregación por departamento y ejercicio (secciones 10, 11 y 13).

Todas las variables anuales se calculan sobre los días válidos, es decir, los
que tienen temperatura, precipitación y viento (y por lo tanto CI calculable).
Los días incompletos se excluyen y se registra la cobertura (sección 11.3).
"""

import pandas as pd

from src.data.load_inia import STATION_COLUMN, exercise_year
from src.features.chill_index import chill_category, chill_index, wind_speed_ms

KEYS = ["DepartamentoCodigo", "AnioEjercicio"]
FULL_WINDOW = "ejercicio"
SENSITIVE_WINDOW = "jul_oct"


def daily_climate(inia_selected: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Clima diario de las estaciones asignadas, con viento en m/s, CI y categoría."""
    climate = cfg["climate"]
    cols = climate["columns"]
    df = inia_selected[[STATION_COLUMN, "DepartamentoCodigo", "Fecha"]].copy()
    df["temperatura_c"] = inia_selected[cols["temperature"]]
    df["precipitacion_mm"] = inia_selected[cols["precipitation"]]
    df["recorrido_viento_km_dia"] = inia_selected[cols["wind_run"]]

    n_neg = int((df["recorrido_viento_km_dia"] < 0).sum() + (df["precipitacion_mm"] < 0).sum())
    if n_neg:
        raise ValueError(f"INIA: {n_neg} valores negativos de viento o precipitación")

    df["AnioEjercicio"] = exercise_year(df["Fecha"], climate["exercise_start_month"])
    df["viento_ms"] = wind_speed_ms(df["recorrido_viento_km_dia"], climate["wind_conversion_divisor"])
    df["chill_index"] = chill_index(df["temperatura_c"], df["viento_ms"], df["precipitacion_mm"])
    df["ci_categoria"] = chill_category(df["chill_index"], climate["chill_thresholds"])
    df["dia_valido"] = df["chill_index"].notna()
    return df.sort_values(["DepartamentoCodigo", "Fecha"]).reset_index(drop=True)


def max_consecutive_days(flags: pd.Series, dates: pd.Series) -> int:
    """Racha más larga de días calendario consecutivos con `flags` verdadero.

    Un día faltante (fecha ausente) corta la racha.
    """
    best = run = 0
    previous = None
    for flag, date in zip(flags, dates):
        if not flag:
            run = 0
        elif run and (date - previous).days == 1:
            run += 1
        else:
            run = 1
        best = max(best, run)
        previous = date
    return best


def expected_days(exercise: int, start_month: int, months: list[int] | None = None) -> int:
    """Días calendario del ejercicio (o de los meses indicados dentro del ejercicio)."""
    start = pd.Timestamp(year=exercise - 1, month=start_month, day=1)
    days = pd.date_range(start, start + pd.DateOffset(years=1) - pd.Timedelta(days=1))
    if months is not None:
        days = days[days.month.isin(months)]
    return len(days)


def aggregate_window(daily: pd.DataFrame, cfg: dict, window: str, months: list[int] | None = None) -> pd.DataFrame:
    """Variables climáticas y de CI por departamento y ejercicio para una ventana."""
    start_month = cfg["climate"]["exercise_start_month"]
    thresholds = cfg["climate"]["chill_thresholds"]
    df = daily if months is None else daily[daily["Fecha"].dt.month.isin(months)]

    rows = []
    for (dep, year), group in df.groupby(KEYS):
        valid = group[group["dia_valido"]].sort_values("Fecha")
        ci = valid["chill_index"]
        n_valid = len(valid)
        n_expected = expected_days(year, start_month, months)
        row = {
            "DepartamentoCodigo": dep,
            "AnioEjercicio": year,
            "dias_esperados": n_expected,
            "dias_validos": n_valid,
            "cobertura": n_valid / n_expected,
            "temp_media_c": valid["temperatura_c"].mean(),
            "precip_total_mm": valid["precipitacion_mm"].sum(),
            "viento_medio_ms": valid["viento_ms"].mean(),
            "ci_medio": ci.mean(),
            "ci_max": ci.max(),
            "ci_p95": ci.quantile(0.95),
        }
        for t in thresholds:
            row[f"dias_ci_ge_{t}"] = int((ci >= t).sum())
        for t in (1000, 1200):
            row[f"prop_ci_ge_{t}"] = (ci >= t).mean()
            row[f"racha_max_ci_ge_{t}"] = max_consecutive_days(ci >= t, valid["Fecha"])
        rows.append(row)

    out = pd.DataFrame(rows)
    return out.rename(columns={c: f"{c}_{window}" for c in out.columns if c not in KEYS})


def climate_by_exercise(daily: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Ejercicio completo y ventana julio–octubre, una fila por departamento y ejercicio."""
    stations = daily.groupby("DepartamentoCodigo")[STATION_COLUMN].first().reset_index()
    full = aggregate_window(daily, cfg, FULL_WINDOW)
    sensitive = aggregate_window(daily, cfg, SENSITIVE_WINDOW, cfg["climate"]["sensitive_months"])
    out = full.merge(sensitive, on=KEYS, how="left", validate="one_to_one")
    return stations.merge(out, on="DepartamentoCodigo", validate="one_to_many")
