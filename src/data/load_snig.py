"""Carga y tipado de los archivos SNIG (DatosAnimales, DatosGenerales y catálogos).

Los CSV se leen como texto y se tipan explícitamente para no perder ceros a la
izquierda en códigos como `ActividadCodigo` o `GiroCodigo` (sección 14.1).
"""

from pathlib import Path

import pandas as pd

from src.config import load_config, project_path

SNIG_SEP = ";"
SNIG_ENCODING = "utf-8-sig"

# Columnas que identifican una fila publicada (sin el ID ni las medidas).
DIMENSION_COLUMNS = [
    "Anio",
    "DepartamentoCodigo",
    "SeccionalPolicialCodigo",
    "AreaSupervision",
    "AreaEnumeracion",
    "ActividadCodigo",
    "GiroCodigo",
    "NaturalezaJuridicaCodigo",
    "EstratoCodigo",
]
MGAP_COLUMNS = ["EspecializacionMGAPCodigo", "TipoProduccionMGAPCodigo"]

INT_COLUMNS = ["Anio", "DepartamentoCodigo"]

ANIMALES_COUNT_COLUMNS = [
    "AnimalesPorEspecieConsumoPD_AD",
    "AnimalesPorEspecieNacimientosPD_AD",
    "AnimalesPorEspecieMortandadPD_AD",
    "CantidadTenedoresPorEspecie",
    "AnimalesPorEspeciePD_AD",
    "AnimalesPorEspeciePD_PF",
]
GENERALES_INT_COLUMNS = ["Superficie", "CantidadTenedores"]
GENERALES_DECIMAL_COLUMNS = ["UnidadesGanaderas", "SuperficieGanadera"]

# Medidas que no pueden ser negativas (sección 14.2, paso 7).
ANIMALES_NON_NEGATIVE = ["AnimalesPorEspecieMortandadPD_AD", "AnimalesPorEspeciePD_AD"]
GENERALES_NON_NEGATIVE = ["SuperficieGanadera", "UnidadesGanaderas"]


def read_snig_csv(path: Path) -> pd.DataFrame:
    """Lee un CSV de SNIG sin inferir tipos: todo queda como texto y los vacíos como ''."""
    return pd.read_csv(
        path, sep=SNIG_SEP, encoding=SNIG_ENCODING, dtype=str, keep_default_na=False
    )


def parse_decimal_comma(values: pd.Series) -> pd.Series:
    """Convierte texto con coma decimal ('19,64') a float.

    Los valores enmascarados con asteriscos ('********', desborde del ancho del
    campo en la publicación SNIG) quedan como NA. Cualquier otro texto no
    numérico hace fallar la carga.
    """
    masked = values.str.fullmatch(r"\*+")
    cleaned = values.mask(masked).str.replace(",", ".", regex=False)
    return pd.to_numeric(cleaned, errors="raise")


def _empty_to_na(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        df[col] = df[col].replace("", pd.NA)
    return df


def _to_int(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors="raise").astype("int64")
    return df


def load_animales(path: Path | None = None) -> pd.DataFrame:
    """DatosAnimales tipado. No filtra departamentos ni especie (ver `filter_ovinos`)."""
    if path is None:
        path = project_path(load_config()["paths"]["raw_animales"])
    df = read_snig_csv(path)
    df = _to_int(df, INT_COLUMNS + ["EspecieCodigo"] + ANIMALES_COUNT_COLUMNS)
    return _empty_to_na(df, MGAP_COLUMNS)


def load_generales(path: Path | None = None) -> pd.DataFrame:
    """DatosGenerales tipado, con `UnidadesGanaderas` y `SuperficieGanadera` como float."""
    if path is None:
        path = project_path(load_config()["paths"]["raw_generales"])
    df = read_snig_csv(path)
    df = _to_int(df, INT_COLUMNS + GENERALES_INT_COLUMNS)
    for col in GENERALES_DECIMAL_COLUMNS:
        df[col] = parse_decimal_comma(df[col])
    return _empty_to_na(df, MGAP_COLUMNS)


def load_catalogo(path: Path) -> pd.DataFrame:
    df = read_snig_csv(path)
    code_col = df.columns[0]
    df[code_col] = pd.to_numeric(df[code_col], errors="raise").astype("int64")
    return df


def check_non_negative(df: pd.DataFrame, columns: list[str], source: str) -> None:
    """Detiene el pipeline si alguna medida es negativa."""
    for col in columns:
        n_neg = int((df[col] < 0).sum())
        if n_neg:
            raise ValueError(f"{source}: {n_neg} valores negativos en {col}")


def check_no_missing(df: pd.DataFrame, columns: list[str], source: str) -> None:
    """Detiene el pipeline si alguna medida quedó faltante (p. ej. enmascarada)."""
    for col in columns:
        n_na = int(df[col].isna().sum())
        if n_na:
            raise ValueError(f"{source}: {n_na} valores faltantes en {col}")


def filter_departments(df: pd.DataFrame, department_codes) -> pd.DataFrame:
    return df[df["DepartamentoCodigo"].isin(list(department_codes))].copy()


def select_ovinos(animales: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Filas ovinas de los cinco departamentos, todos los años, sin validar."""
    df = filter_departments(animales, cfg["departments"])
    return df[df["EspecieCodigo"] == cfg["species"]["sheep_code"]].copy()


def _study_years(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    start, end = cfg["project"]["start_year"], cfg["project"]["end_year"]
    return df[df["Anio"].between(start, end)].copy()


def filter_generales(generales: pd.DataFrame, cfg: dict | None = None) -> pd.DataFrame:
    """DatosGenerales modelable: cinco departamentos, período de estudio, completo y no negativo.

    Los negativos de 2016 quedan fuera por el filtro de años y se informan en la auditoría.
    """
    cfg = cfg or load_config()
    df = _study_years(filter_departments(generales, cfg["departments"]), cfg)
    check_no_missing(df, GENERALES_NON_NEGATIVE, "DatosGenerales (alcance)")
    check_non_negative(df, GENERALES_NON_NEGATIVE, "DatosGenerales (alcance)")
    return df


def filter_ovinos(animales: pd.DataFrame, cfg: dict | None = None) -> pd.DataFrame:
    """DatosAnimales modelable: ovinos de los cinco departamentos en el período de estudio, validados."""
    cfg = cfg or load_config()
    df = _study_years(select_ovinos(animales, cfg), cfg)
    check_no_missing(df, ANIMALES_NON_NEGATIVE, "DatosAnimales (ovinos)")
    check_non_negative(df, ANIMALES_NON_NEGATIVE, "DatosAnimales (ovinos)")
    return df
