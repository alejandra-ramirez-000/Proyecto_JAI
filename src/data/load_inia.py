"""Carga de INIA.csv, construcción de fechas y asignación estación–departamento.

Los nombres de estación del archivo vienen en Unicode descompuesto (NFD) para
algunas estaciones ('Tacuarembó' = 'o' + acento combinado), por lo que se
normalizan a NFC antes de compararlos con la configuración (sección 25).
"""

import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import load_config, project_path

STATION_COLUMN = "EstacionAgr"


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def exercise_year(dates: pd.Series, start_month: int = 7) -> pd.Series:
    """Ejercicio ganadero julio–junio: julio a diciembre pertenecen al ejercicio siguiente."""
    return np.where(dates.dt.month >= start_month, dates.dt.year + 1, dates.dt.year)


def load_inia(path: Path | None = None) -> pd.DataFrame:
    """INIA con `Fecha` construida y nombres de estación en NFC. Incluye todas las estaciones.

    Falla si hay fechas imposibles o duplicados estación–fecha.
    """
    if path is None:
        path = project_path(load_config()["paths"]["raw_inia"])
    df = pd.read_csv(path, sep=",", encoding="utf-8-sig")
    df[STATION_COLUMN] = df[STATION_COLUMN].map(nfc)

    df["Fecha"] = pd.to_datetime(
        dict(year=df["Anio"], month=df["Mes"], day=df["Dia"]), errors="coerce"
    )
    n_bad = int(df["Fecha"].isna().sum())
    if n_bad:
        raise ValueError(f"INIA: {n_bad} filas con fecha imposible")

    n_dup = int(df.duplicated([STATION_COLUMN, "Fecha"]).sum())
    if n_dup:
        raise ValueError(f"INIA: {n_dup} duplicados estación–fecha")
    return df


def station_department_map(cfg: dict) -> dict[str, int]:
    return {nfc(d["station"]): code for code, d in cfg["departments"].items()}


def select_stations(inia: pd.DataFrame, cfg: dict | None = None) -> pd.DataFrame:
    """Conserva solo las estaciones asignadas y agrega `DepartamentoCodigo`.

    Falla si falta una estación configurada o si aparece una estación que no
    está ni asignada ni explícitamente excluida.
    """
    cfg = cfg or load_config()
    mapping = station_department_map(cfg)
    excluded = {nfc(s) for s in cfg["excluded_stations"]}
    present = set(inia[STATION_COLUMN].unique())

    missing = set(mapping) - present
    if missing:
        raise ValueError(f"INIA: faltan estaciones configuradas: {sorted(missing)}")
    unknown = present - set(mapping) - excluded
    if unknown:
        raise ValueError(f"INIA: estaciones no previstas en la configuración: {sorted(unknown)}")

    df = inia[inia[STATION_COLUMN].isin(mapping)].copy()
    df["DepartamentoCodigo"] = df[STATION_COLUMN].map(mapping).astype("int64")
    for col in cfg["climate"]["columns"].values():
        df[col] = pd.to_numeric(df[col], errors="raise")
    return df
