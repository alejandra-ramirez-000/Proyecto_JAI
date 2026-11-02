"""Tablas del análisis exploratorio (sección 22).

Las correlaciones "intra-departamento" se calculan sobre desvíos respecto de la
media de cada departamento: miden variación temporal y no diferencias
estructurales entre regiones (sección 22, último párrafo).
"""

import numpy as np
import pandas as pd

from src.features.build_features import FULL_WINDOW, SENSITIVE_WINDOW

TARGETS = {
    "tasa_mortalidad_1000": "Mortalidad ovina (por mil)",
    "intensidad_ug_ha": "Intensidad (UG/ha)",
}

CLIMATE_VARIABLES = {
    "temp_media_c": "Temperatura media (°C)",
    "precip_total_mm": "Precipitación total (mm)",
    "viento_medio_ms": "Viento medio (m/s)",
    "ci_medio": "CI medio",
    "ci_max": "CI máximo",
    "ci_p95": "CI percentil 95",
    "dias_ci_ge_900": "Días CI ≥ 900",
    "dias_ci_ge_1000": "Días CI ≥ 1000",
    "dias_ci_ge_1100": "Días CI ≥ 1100",
    "dias_ci_ge_1200": "Días CI ≥ 1200",
    "racha_max_ci_ge_1000": "Racha máx. CI ≥ 1000",
    "racha_max_ci_ge_1200": "Racha máx. CI ≥ 1200",
}

LAG_VARIABLES = {
    "mortalidad_lag1": "Mortalidad del ejercicio anterior",
    "intensidad_lag1": "Intensidad del ejercicio anterior",
}

DEPT = "DepartamentoCodigo"


def within_department(panel: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Desvío de cada variable respecto de la media de su departamento."""
    return panel[columns] - panel.groupby(DEPT)[columns].transform("mean")


def within_department_and_year(panel: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Desvío respecto de la media del departamento y de la media del ejercicio (doble diferencia).

    Quita también los shocks comunes a los cinco departamentos en un mismo año,
    que comparten clima regional y contexto de mercado.
    """
    return (
        panel[columns]
        - panel.groupby(DEPT)[columns].transform("mean")
        - panel.groupby("AnioEjercicio")[columns].transform("mean")
        + panel[columns].mean()
    )


def _pearson(x: pd.Series, y: pd.Series) -> tuple[float, int]:
    mask = x.notna() & y.notna()
    if mask.sum() < 3 or x[mask].std() == 0 or y[mask].std() == 0:
        return np.nan, int(mask.sum())
    return float(np.corrcoef(x[mask], y[mask])[0, 1]), int(mask.sum())


def correlation_table(panel: pd.DataFrame) -> pd.DataFrame:
    """Correlación de Pearson global e intra-departamento de cada predictor con cada objetivo."""
    predictors = [(f"{v}_{w}", v, w) for w in (FULL_WINDOW, SENSITIVE_WINDOW) for v in CLIMATE_VARIABLES]
    predictors += [(v, v, "historia") for v in LAG_VARIABLES]
    columns = [c for c, _, _ in predictors] + list(TARGETS)
    demeaned = within_department(panel, columns)
    two_way = within_department_and_year(panel, columns)

    rows = []
    for target in TARGETS:
        for col, base, window in predictors:
            r_global, n = _pearson(panel[col], panel[target])
            r_within, _ = _pearson(demeaned[col], demeaned[target])
            r_two_way, _ = _pearson(two_way[col], two_way[target])
            rows.append(
                {
                    "objetivo": target,
                    "variable": base,
                    "ventana": window,
                    "columna": col,
                    "n": n,
                    "r_global": r_global,
                    "r_intra_departamento": r_within,
                    "r_intra_departamento_y_anio": r_two_way,
                }
            )
    return pd.DataFrame(rows)


def per_department_correlations(panel: pd.DataFrame, window: str = FULL_WINDOW) -> pd.DataFrame:
    """Correlación por departamento (n = 9 por departamento: solo descriptiva)."""
    rows = []
    for (code, name), group in panel.groupby([DEPT, "Departamento"]):
        for target in TARGETS:
            for var in CLIMATE_VARIABLES:
                r, n = _pearson(group[f"{var}_{window}"], group[target])
                rows.append({DEPT: code, "Departamento": name, "objetivo": target, "variable": var, "n": n, "r": r})
    return pd.DataFrame(rows)


def window_comparison(correlations: pd.DataFrame) -> pd.DataFrame:
    """r intra-departamento del ejercicio completo frente a julio–octubre."""
    climate = correlations[correlations["ventana"] != "historia"]
    out = climate.pivot_table(
        index=["objetivo", "variable"], columns="ventana", values="r_intra_departamento"
    ).reset_index()
    out["diferencia_abs"] = out[SENSITIVE_WINDOW].abs() - out[FULL_WINDOW].abs()
    return out


def zscores_by_department(panel: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    grouped = panel.groupby(DEPT)[columns]
    return (panel[columns] - grouped.transform("mean")) / grouped.transform("std")


def extreme_years(panel: pd.DataFrame, threshold: float = 1.5) -> pd.DataFrame:
    """Departamento–ejercicio con |z| >= umbral en algún objetivo o en la exposición al CI.

    El z se calcula dentro de cada departamento sobre los nueve ejercicios.
    """
    columns = list(TARGETS) + [f"dias_ci_ge_1000_{FULL_WINDOW}", f"precip_total_mm_{FULL_WINDOW}"]
    z = zscores_by_department(panel, columns).add_prefix("z_")
    out = pd.concat([panel[[DEPT, "Departamento", "AnioEjercicio"] + columns], z], axis=1)
    flagged = (z.abs() >= threshold).any(axis=1)
    return out[flagged].sort_values([DEPT, "AnioEjercicio"]).reset_index(drop=True)


def coverage_by_station(daily: pd.DataFrame) -> pd.DataFrame:
    """Días válidos sobre días con registro, por estación y ejercicio."""
    return (
        daily.groupby(["EstacionAgr", "AnioEjercicio"])
        .agg(dias_con_registro=("Fecha", "size"), dias_validos=("dia_valido", "sum"))
        .assign(cobertura_registros=lambda d: d["dias_validos"] / d["dias_con_registro"])
        .reset_index()
    )


def missing_by_station_year(daily: pd.DataFrame) -> pd.DataFrame:
    """Días faltantes de cada variable requerida por estación y año calendario."""
    variables = {
        "temperatura_c": "Temperatura",
        "precipitacion_mm": "Precipitación",
        "recorrido_viento_km_dia": "Viento",
    }
    df = daily.assign(anio=daily["Fecha"].dt.year)
    out = df[list(variables)].isna().groupby([df["EstacionAgr"], df["anio"]]).sum()
    return out.rename(columns=variables).reset_index().melt(
        id_vars=["EstacionAgr", "anio"], var_name="variable", value_name="dias_faltantes"
    )


def ci_category_days(daily: pd.DataFrame, years: tuple[int, int]) -> pd.DataFrame:
    """Días por categoría de Chill Index, por departamento y ejercicio."""
    df = daily[daily["AnioEjercicio"].between(*years) & daily["dia_valido"]]
    out = df.groupby([DEPT, "AnioEjercicio", "ci_categoria"], observed=False).size()
    return out.rename("dias").reset_index()
