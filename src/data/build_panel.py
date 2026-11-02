"""Construcción del panel departamento–ejercicio (Entregable 2, secciones 12, 14 y 15).

Uso:
    python -m src.data.build_panel

Genera los intermedios en data/interim/ y el panel final, su diccionario y los
metadatos de ejecución en data/processed/. Se detiene si la cardinalidad del
panel no es la esperada.
"""

import json
import platform
from datetime import datetime
from importlib import metadata

import numpy as np
import pandas as pd

from src.config import load_config, project_path
from src.data.audit import compute_raw_hashes
from src.data.load_inia import STATION_COLUMN, load_inia, select_stations
from src.data.load_snig import filter_generales, filter_ovinos, load_animales, load_generales
from src.features.build_features import FULL_WINDOW, KEYS, SENSITIVE_WINDOW, climate_by_exercise, daily_climate

# Variables con rezago anual por departamento (sección 13.4).
LAG_COLUMNS = {
    "intensidad_ug_ha": "intensidad_lag1",
    "tasa_mortalidad_1000": "mortalidad_lag1",
    "stock_ovino": "stock_ovino_lag1",
    "tenedores_ovinos": "tenedores_ovinos_lag1",
}


def _safe_ratio(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Cociente que queda faltante si el denominador es cero."""
    return numerator / denominator.where(denominator != 0)


def aggregate_animales(ovinos: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Suma por departamento y ejercicio y calcula la tasa proxy de mortalidad (sección 12.2)."""
    out = (
        ovinos.rename(columns={"Anio": "AnioEjercicio"})
        .groupby(KEYS, as_index=False)
        .agg(
            muertes_ovinas=("AnimalesPorEspecieMortandadPD_AD", "sum"),
            stock_ovino=("AnimalesPorEspeciePD_AD", "sum"),
            tenedores_ovinos=("CantidadTenedoresPorEspecie", "sum"),
            nacimientos_ovinos=("AnimalesPorEspecieNacimientosPD_AD", "sum"),
            stock_ovino_pd_pf=("AnimalesPorEspeciePD_PF", "sum"),
        )
    )
    out["tasa_mortalidad_1000"] = cfg["targets"]["mortality_per"] * _safe_ratio(
        out["muertes_ovinas"], out["stock_ovino"]
    )
    return out


def aggregate_generales(generales: pd.DataFrame) -> pd.DataFrame:
    """Suma por departamento y ejercicio y calcula la intensidad ganadera (sección 12.1).

    La intensidad es el cociente de los totales, nunca el promedio de cocientes por fila.
    """
    out = (
        generales.rename(columns={"Anio": "AnioEjercicio"})
        .groupby(KEYS, as_index=False)
        .agg(
            unidades_ganaderas=("UnidadesGanaderas", "sum"),
            superficie_ganadera=("SuperficieGanadera", "sum"),
            superficie_total=("Superficie", "sum"),
            tenedores_total=("CantidadTenedores", "sum"),
        )
    )
    out["intensidad_ug_ha"] = _safe_ratio(out["unidades_ganaderas"], out["superficie_ganadera"])
    return out


def add_lags(panel: pd.DataFrame) -> pd.DataFrame:
    """Rezago de un ejercicio dentro de cada departamento.

    Solo usa el ejercicio inmediatamente anterior: si falta, el rezago queda
    faltante (no se rellena con cero ni con promedios).
    """
    panel = panel.sort_values(KEYS).reset_index(drop=True)
    by_dep = panel.groupby("DepartamentoCodigo")
    previous_year = by_dep["AnioEjercicio"].shift(1)
    consecutive = panel["AnioEjercicio"] - previous_year == 1
    for col, lag_col in LAG_COLUMNS.items():
        panel[lag_col] = by_dep[col].shift(1).where(consecutive)
    return panel


def check_cardinality(panel: pd.DataFrame, cfg: dict) -> None:
    """Controles de la sección 14.5. Detiene el pipeline con un mensaje descriptivo."""
    exp = cfg["expected_panel"]
    lagged = panel.dropna(subset=list(LAG_COLUMNS.values()))
    checks = [
        ("filas del panel", len(panel), exp["rows"]),
        ("departamentos", panel["DepartamentoCodigo"].nunique(), exp["departments"]),
        ("ejercicios", panel["AnioEjercicio"].nunique(), exp["exercises"]),
        ("duplicados departamento–ejercicio", int(panel.duplicated(KEYS).sum()), 0),
        ("filas con rezago", len(lagged), exp["rows_with_lag"]),
        ("ejercicios con rezago", lagged["AnioEjercicio"].nunique(), exp["exercises_with_lag"]),
    ]
    errors = [f"{name}: {got} (esperado {want})" for name, got, want in checks if got != want]
    if errors:
        raise ValueError("Cardinalidad del panel incorrecta: " + "; ".join(errors))


def check_coverage(panel: pd.DataFrame, cfg: dict) -> None:
    minimum = cfg["climate"]["minimum_coverage"]
    for window in (FULL_WINDOW, SENSITIVE_WINDOW):
        col = f"cobertura_{window}"
        low = panel[panel[col] < minimum]
        if not low.empty:
            raise ValueError(
                f"Cobertura climática < {minimum} en {col}: "
                f"{low[KEYS].to_dict('records')}"
            )


def build_panel(cfg: dict | None = None) -> dict[str, pd.DataFrame]:
    """Construye todas las tablas del panel sin escribir a disco."""
    cfg = cfg or load_config()
    paths = cfg["paths"]
    start, end = cfg["project"]["start_year"], cfg["project"]["end_year"]

    ovinos = filter_ovinos(load_animales(project_path(paths["raw_animales"])), cfg)
    generales = filter_generales(load_generales(project_path(paths["raw_generales"])), cfg)
    animales_agg = aggregate_animales(ovinos, cfg)
    generales_agg = aggregate_generales(generales)

    daily = daily_climate(select_stations(load_inia(project_path(paths["raw_inia"])), cfg), cfg)
    climate = climate_by_exercise(daily, cfg)

    snig = generales_agg.merge(animales_agg, on=KEYS, how="inner", validate="one_to_one")
    climate_period = climate[climate["AnioEjercicio"].between(start, end)]
    unmatched = snig.merge(climate_period, on=KEYS, how="outer", indicator=True)
    unmatched = unmatched[unmatched["_merge"] != "both"]
    if not unmatched.empty:
        raise ValueError(f"Combinaciones sin pareja SNIG–INIA: {unmatched[KEYS + ['_merge']].to_dict('records')}")

    panel = snig.merge(climate_period, on=KEYS, how="inner", validate="one_to_one")
    names = {code: d["name"] for code, d in cfg["departments"].items()}
    panel.insert(1, "Departamento", panel["DepartamentoCodigo"].map(names))
    panel = add_lags(panel)
    first_cols = ["DepartamentoCodigo", "Departamento", "AnioEjercicio", STATION_COLUMN]
    panel = panel[first_cols + [c for c in panel.columns if c not in first_cols]]

    check_cardinality(panel, cfg)
    check_coverage(panel, cfg)
    return {
        "clima_diario_con_ci": daily,
        "clima_por_ejercicio": climate,
        "animales_por_departamento_anio": animales_agg,
        "generales_por_departamento_anio": generales_agg,
        "panel": panel,
    }


# ---------------------------------------------------------------------------
# Diccionario del panel
# ---------------------------------------------------------------------------

_ROLE_ID = "identificación"
_ROLE_TARGET = "objetivo"
_ROLE_COMPONENT = "componente del objetivo"
_ROLE_CLIMATE = "predictor climático"
_ROLE_LAG = "predictor histórico (rezago)"
_ROLE_QC = "control de calidad"
_ROLE_DESC = "descriptiva — no usar como predictor"

_BASE_DICTIONARY = {
    "DepartamentoCodigo": ("Código SNIG del departamento (categórico, no continuo)", "-", _ROLE_ID),
    "Departamento": ("Nombre del departamento", "-", _ROLE_ID),
    "AnioEjercicio": ("Ejercicio ganadero: 1 de julio del año anterior al 30 de junio", "año", _ROLE_ID),
    STATION_COLUMN: ("Estación INIA asignada al departamento", "-", _ROLE_ID),
    "unidades_ganaderas": ("Suma de UnidadesGanaderas (DatosGenerales)", "UG", _ROLE_COMPONENT),
    "superficie_ganadera": ("Suma de SuperficieGanadera (DatosGenerales)", "ha", _ROLE_COMPONENT),
    "superficie_total": ("Suma de Superficie (DatosGenerales)", "ha", _ROLE_DESC),
    "tenedores_total": ("Suma de CantidadTenedores (DatosGenerales)", "tenedores", _ROLE_DESC),
    "intensidad_ug_ha": ("unidades_ganaderas / superficie_ganadera", "UG/ha", _ROLE_TARGET + " (regresión)"),
    "muertes_ovinas": ("Suma de AnimalesPorEspecieMortandadPD_AD, ovinos", "animales", _ROLE_COMPONENT),
    "stock_ovino": ("Suma de AnimalesPorEspeciePD_AD, ovinos (existencia declarada al cierre)", "animales", _ROLE_COMPONENT),
    "tenedores_ovinos": ("Suma de CantidadTenedoresPorEspecie, ovinos", "tenedores", _ROLE_DESC),
    "nacimientos_ovinos": ("Suma de AnimalesPorEspecieNacimientosPD_AD, ovinos (simultáneo al objetivo)", "animales", _ROLE_DESC),
    "stock_ovino_pd_pf": ("Suma de AnimalesPorEspeciePD_PF, ovinos; solo para sensibilidad del denominador", "animales", _ROLE_DESC),
    "tasa_mortalidad_1000": (
        "Tasa proxy de mortalidad ovina: 1000 × muertes_ovinas / stock_ovino. "
        "La etiqueta de mortalidad elevada NO está en el panel: se calcula dentro de cada fold",
        "muertes por mil", _ROLE_TARGET + " (continuo y base de la clasificación)",
    ),
    "intensidad_lag1": ("intensidad_ug_ha del ejercicio anterior, mismo departamento", "UG/ha", _ROLE_LAG),
    "mortalidad_lag1": ("tasa_mortalidad_1000 del ejercicio anterior, mismo departamento", "muertes por mil", _ROLE_LAG),
    "stock_ovino_lag1": ("stock_ovino del ejercicio anterior, mismo departamento", "animales", _ROLE_LAG),
    "tenedores_ovinos_lag1": ("tenedores_ovinos del ejercicio anterior, mismo departamento", "tenedores", _ROLE_LAG),
}

_CLIMATE_DICTIONARY = {
    "dias_esperados": ("Días calendario de la ventana", "días", _ROLE_QC),
    "dias_validos": ("Días con temperatura, precipitación y viento (CI calculable)", "días", _ROLE_QC),
    "cobertura": ("dias_validos / dias_esperados (mínimo exigido 0,95)", "proporción", _ROLE_QC),
    "temp_media_c": ("Promedio de TempAireMedia en días válidos", "°C", _ROLE_CLIMATE),
    "precip_total_mm": ("Suma de PrecipAcum en días válidos", "mm", _ROLE_CLIMATE),
    "viento_medio_ms": ("Promedio de RecorridoViento / 86,4 en días válidos", "m/s", _ROLE_CLIMATE),
    "ci_medio": ("Promedio del Chill Index diario", "kJ/m²/h", _ROLE_CLIMATE),
    "ci_max": ("Máximo del Chill Index diario", "kJ/m²/h", _ROLE_CLIMATE),
    "ci_p95": ("Percentil 95 del Chill Index diario", "kJ/m²/h", _ROLE_CLIMATE),
}

_WINDOW_LABELS = {FULL_WINDOW: "ejercicio completo (jul–jun)", SENSITIVE_WINDOW: "julio–octubre"}


def _climate_entry(base: str, window: str) -> tuple[str, str, str]:
    if base in _CLIMATE_DICTIONARY:
        desc, unit, role = _CLIMATE_DICTIONARY[base]
    elif base.startswith("dias_ci_ge_"):
        desc, unit, role = f"Días con CI >= {base.rsplit('_', 1)[1]}", "días", _ROLE_CLIMATE
    elif base.startswith("prop_ci_ge_"):
        desc, unit, role = f"Proporción de días válidos con CI >= {base.rsplit('_', 1)[1]}", "proporción", _ROLE_CLIMATE
    elif base.startswith("racha_max_ci_ge_"):
        desc, unit, role = (
            f"Máxima cantidad de días consecutivos con CI >= {base.rsplit('_', 1)[1]}", "días", _ROLE_CLIMATE
        )
    else:
        raise KeyError(base)
    return f"{desc}; {_WINDOW_LABELS[window]}", unit, role


def panel_dictionary(panel: pd.DataFrame) -> pd.DataFrame:
    """Descripción, unidad y rol de cada columna. Falla si alguna columna no está documentada."""
    rows = []
    for col in panel.columns:
        if col in _BASE_DICTIONARY:
            desc, unit, role = _BASE_DICTIONARY[col]
        else:
            window = next((w for w in (FULL_WINDOW, SENSITIVE_WINDOW) if col.endswith(f"_{w}")), None)
            if window is None:
                raise KeyError(f"Columna sin documentar en el diccionario: {col}")
            desc, unit, role = _climate_entry(col[: -len(window) - 1], window)
        rows.append({"columna": col, "descripcion": desc, "unidad": unit, "rol": role})
    return pd.DataFrame(rows)


def _dictionary_markdown(dictionary: pd.DataFrame, panel: pd.DataFrame, cfg: dict) -> str:
    lines = [
        "# Diccionario del panel departamento–ejercicio",
        "",
        "Archivo: `data/processed/panel_departamento_ejercicio.csv`. Generado por `python -m src.data.build_panel`; no editar a mano.",
        "",
        f"- Una fila por `DepartamentoCodigo` + `AnioEjercicio`: {len(panel)} filas, "
        f"ejercicios {cfg['project']['start_year']}–{cfg['project']['end_year']}.",
        f"- Los rezagos son faltantes en el primer ejercicio de cada departamento; "
        f"el panel con rezagos tiene {len(panel.dropna(subset=list(LAG_COLUMNS.values())))} filas.",
        "- Las variables climáticas se calculan sobre días válidos; los días incompletos no se imputan.",
        "- Fuentes: SNIG/DICOSE (DatosAnimales, DatosGenerales) e INIA (banco de datos agroclimáticos).",
        "",
        "| columna | descripción | unidad | rol |",
        "|---|---|---|---|",
    ]
    lines += [f"| `{r.columna}` | {r.descripcion} | {r.unidad} | {r.rol} |" for r in dictionary.itertuples()]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Escritura
# ---------------------------------------------------------------------------


def run_metadata(cfg: dict, panel: pd.DataFrame) -> dict:
    packages = ["pandas", "numpy", "pyarrow", "PyYAML"]
    return {
        "generado": datetime.now().isoformat(timespec="seconds"),
        "python": platform.python_version(),
        "paquetes": {p: metadata.version(p) for p in packages},
        "raw_sha256": compute_raw_hashes(cfg),
        "configuracion": cfg,
        "filas": len(panel),
        "filas_con_rezago": len(panel.dropna(subset=list(LAG_COLUMNS.values()))),
        "columnas": list(panel.columns),
    }


def write_outputs(tables: dict[str, pd.DataFrame], cfg: dict) -> None:
    interim = project_path(cfg["paths"]["interim_dir"])
    processed = project_path(cfg["paths"]["processed_dir"])
    interim.mkdir(parents=True, exist_ok=True)
    processed.mkdir(parents=True, exist_ok=True)

    daily = tables["clima_diario_con_ci"].copy()
    daily["ci_categoria"] = daily["ci_categoria"].astype("string")
    daily.to_parquet(interim / "clima_diario_con_ci.parquet", index=False)
    for name in ("clima_por_ejercicio", "animales_por_departamento_anio", "generales_por_departamento_anio"):
        tables[name].to_csv(interim / f"{name}.csv", index=False, encoding="utf-8")

    panel = tables["panel"]
    panel.to_csv(processed / "panel_departamento_ejercicio.csv", index=False, encoding="utf-8")
    dictionary = panel_dictionary(panel)
    (processed / "diccionario_panel.md").write_text(_dictionary_markdown(dictionary, panel, cfg), encoding="utf-8")
    meta = run_metadata(cfg, panel)
    (processed / "panel_metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )


def main() -> None:
    cfg = load_config()
    tables = build_panel(cfg)
    write_outputs(tables, cfg)
    panel = tables["panel"]
    summary = panel.groupby("Departamento")[["intensidad_ug_ha", "tasa_mortalidad_1000"]].agg(["min", "max"])
    with pd.option_context("display.width", 200, "display.float_format", "{:.3f}".format):
        print(f"Panel: {len(panel)} filas, {panel.shape[1]} columnas")
        print(summary)
    print(f"Escrito en {project_path(cfg['paths']['processed_dir'])}")


if __name__ == "__main__":
    main()
