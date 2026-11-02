"""Auditoría de los datos crudos (Entregable 1).

Vuelve a verificar automáticamente los hallazgos de la sección 9 de la
especificación y genera tablas CSV y un resumen en Markdown.

Uso:
    python -m src.data.audit                     # genera reports/auditoria/
    python -m src.data.audit --registrar-hashes  # crea config/raw_sha256.txt
"""

import argparse
import hashlib
import platform
from datetime import datetime
from importlib import metadata
from pathlib import Path

import pandas as pd

from src.config import PROJECT_ROOT, load_config, project_path
from src.data.load_inia import STATION_COLUMN, exercise_year, load_inia, nfc, station_department_map
from src.data.load_snig import (
    ANIMALES_COUNT_COLUMNS,
    DIMENSION_COLUMNS,
    GENERALES_DECIMAL_COLUMNS,
    GENERALES_INT_COLUMNS,
    MGAP_COLUMNS,
    filter_departments,
    filter_generales,
    filter_ovinos,
    load_animales,
    load_catalogo,
    load_generales,
    select_ovinos,
)

# ---------------------------------------------------------------------------
# Hashes de los archivos raw
# ---------------------------------------------------------------------------


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def raw_files(cfg: dict) -> list[Path]:
    return sorted(p for p in project_path(cfg["paths"]["raw_dir"]).rglob("*") if p.is_file())


def compute_raw_hashes(cfg: dict) -> dict[str, str]:
    return {p.relative_to(PROJECT_ROOT).as_posix(): sha256(p) for p in raw_files(cfg)}


def write_hash_manifest(cfg: dict) -> Path:
    path = project_path(cfg["paths"]["raw_hash_manifest"])
    lines = [f"{digest}  {name}" for name, digest in compute_raw_hashes(cfg).items()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def read_hash_manifest(cfg: dict) -> dict[str, str]:
    path = project_path(cfg["paths"]["raw_hash_manifest"])
    if not path.is_file():
        return {}
    entries = (line.split("  ", 1) for line in path.read_text(encoding="utf-8").splitlines() if line)
    return {name: digest for digest, name in entries}


def check_raw_hashes(cfg: dict) -> pd.DataFrame:
    registered = read_hash_manifest(cfg)
    current = compute_raw_hashes(cfg)
    rows = [
        {
            "archivo": name,
            "sha256_registrado": registered.get(name),
            "sha256_actual": current.get(name),
            "coincide": registered.get(name) == current.get(name),
        }
        for name in sorted(set(registered) | set(current))
    ]
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Tablas de auditoría
# ---------------------------------------------------------------------------


def schema_table(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "columna": df.columns,
            "dtype": [str(t) for t in df.dtypes],
            "nulos": df.isna().sum().values,
            "nulos_pct": (100 * df.isna().mean()).round(2).values,
            "valores_unicos": df.nunique().values,
        }
    )


def mgap_null_by_year(animales: pd.DataFrame, generales: pd.DataFrame) -> pd.DataFrame:
    parts = []
    for name, df in [("DatosAnimales", animales), ("DatosGenerales", generales)]:
        part = df[MGAP_COLUMNS].isna().groupby(df["Anio"]).mean().mul(100).round(2)
        part.columns = [f"{name}.{c}_nulos_pct" for c in part.columns]
        parts.append(part)
    return pd.concat(parts, axis=1).reset_index()


def duplicate_summary(
    animales: pd.DataFrame, generales: pd.DataFrame, inia: pd.DataFrame
) -> pd.DataFrame:
    rows = []
    for name, df, extra in [
        ("DatosAnimales", animales, ["EspecieCodigo"]),
        ("DatosGenerales", generales, []),
    ]:
        dims = DIMENSION_COLUMNS + extra
        rows += [
            {"archivo": name, "clave": "dimensiones + MGAP", "duplicados": int(df.duplicated(dims + MGAP_COLUMNS).sum())},
            {"archivo": name, "clave": "dimensiones sin MGAP", "duplicados": int(df.duplicated(dims).sum())},
            {"archivo": name, "clave": "fila completa sin ID", "duplicados": int(df.drop(columns="ID").duplicated().sum())},
        ]
    rows.append(
        {"archivo": "INIA", "clave": "estación + fecha", "duplicados": int(inia.duplicated([STATION_COLUMN, "Fecha"]).sum())}
    )
    return pd.DataFrame(rows)


def impossible_values(
    animales: pd.DataFrame, generales: pd.DataFrame, inia: pd.DataFrame, cfg: dict
) -> pd.DataFrame:
    rows = []
    for name, df, cols in [
        ("DatosAnimales", animales, ANIMALES_COUNT_COLUMNS),
        ("DatosGenerales", generales, GENERALES_INT_COLUMNS + GENERALES_DECIMAL_COLUMNS),
    ]:
        for col in cols:
            rows.append({"archivo": name, "columna": col, "regla": ">= 0", "violaciones": int((df[col] < 0).sum())})
    for col, (low, high) in cfg["plausible_ranges"].items():
        values = inia[col]
        rows.append(
            {
                "archivo": "INIA",
                "columna": col,
                "regla": f"entre {low} y {high}",
                "violaciones": int(((values < low) | (values > high)).sum()),
            }
        )
    return pd.DataFrame(rows)


def climate_missing_by_station(inia: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    cols = list(cfg["climate"]["columns"].values())
    grouped = inia.groupby(STATION_COLUMN)
    out = grouped[cols].agg(lambda s: int(s.isna().sum()))
    out.columns = [f"{c}_faltantes" for c in cols]
    out.insert(0, "dias", grouped.size())
    out.insert(1, "primera_fecha", grouped["Fecha"].min().dt.date)
    out.insert(2, "ultima_fecha", grouped["Fecha"].max().dt.date)
    return out.reset_index()


def climate_coverage(inia: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Cobertura por estación y ejercicio ganadero (julio–junio).

    Un día es válido si tiene temperatura, precipitación y viento, que son las
    entradas del Chill Index (sección 11.3).
    """
    cols = list(cfg["climate"]["columns"].values())
    start_month = cfg["climate"]["exercise_start_month"]
    df = inia[[STATION_COLUMN, "Fecha"] + cols].copy()
    df["AnioEjercicio"] = exercise_year(df["Fecha"], start_month)
    df["valido"] = df[cols].notna().all(axis=1)

    # Grilla completa estación × ejercicio para que un ejercicio sin registros figure con 0 %.
    grid = pd.MultiIndex.from_product(
        [sorted(df[STATION_COLUMN].unique()), sorted(df["AnioEjercicio"].unique())],
        names=[STATION_COLUMN, "AnioEjercicio"],
    )
    out = (
        df.groupby([STATION_COLUMN, "AnioEjercicio"])
        .agg(dias_con_registro=("Fecha", "size"), dias_validos=("valido", "sum"))
        .reindex(grid, fill_value=0)
        .reset_index()
    )
    starts = pd.to_datetime(dict(year=out["AnioEjercicio"] - 1, month=start_month, day=1))
    ends = starts + pd.DateOffset(years=1)
    out["dias_esperados"] = (ends - starts).dt.days
    out["cobertura"] = (out["dias_validos"] / out["dias_esperados"]).round(4)
    out["cumple_minimo"] = out["cobertura"] >= cfg["climate"]["minimum_coverage"]
    return out


def _years_label(years) -> str:
    years = sorted(set(years))
    return f"{years[0]}–{years[-1]}" if years else "-"


def section9_checks(
    animales: pd.DataFrame,
    generales: pd.DataFrame,
    inia: pd.DataFrame,
    coverage: pd.DataFrame,
    hashes: pd.DataFrame,
    cfg: dict,
) -> pd.DataFrame:
    exp = cfg["expected_raw"]
    first, last = cfg["project"]["snig_years"]
    start, end = cfg["project"]["start_year"], cfg["project"]["end_year"]
    years_label = f"{first}–{last}"

    ovinos = select_ovinos(animales, cfg)
    generales_scope = filter_departments(generales, cfg["departments"])
    mgap_null = animales[MGAP_COLUMNS].isna().all(axis=1).groupby(animales["Anio"]).mean()
    mgap_any_null = animales[MGAP_COLUMNS].isna().any(axis=1).groupby(animales["Anio"]).mean()

    selected = set(station_department_map(cfg))
    in_period = coverage["AnioEjercicio"].between(start, end)
    cov_selected = coverage[in_period & coverage[STATION_COLUMN].isin(selected)]
    excluded = {nfc(s) for s in cfg["excluded_stations"]}
    cov_excluded = coverage[in_period & coverage[STATION_COLUMN].isin(excluded)]
    n_exercises = end - start + 1

    dups = duplicate_summary(animales, generales, inia).set_index(["archivo", "clave"])["duplicados"]

    def row(chequeo, esperado, observado, ok=None):
        return {
            "chequeo": chequeo,
            "esperado": esperado,
            "observado": observado,
            "ok": bool(esperado == observado) if ok is None else bool(ok),
        }

    def validates(filter_fn, df) -> str:
        try:
            filter_fn(df, cfg)
        except ValueError as exc:
            return str(exc)
        return "sin errores"

    rows = [
        row("Filas DatosAnimales", exp["animales_rows"], len(animales)),
        row("Filas DatosGenerales", exp["generales_rows"], len(generales)),
        row("Años DatosAnimales", years_label, _years_label(animales["Anio"])),
        row("Años DatosGenerales", years_label, _years_label(generales["Anio"])),
        row("Filas ovinas en los 5 departamentos", exp["ovinos_rows_scope"], len(ovinos)),
        row("Combinaciones departamento–año (ovinos)", exp["department_years_scope"],
            ovinos.groupby(["DepartamentoCodigo", "Anio"]).ngroups),
        row("Combinaciones departamento–año (generales)", exp["department_years_scope"],
            generales_scope.groupby(["DepartamentoCodigo", "Anio"]).ngroups),
        row(f"Departamento–ejercicio {start}–{end} con cobertura climática mínima",
            cfg["expected_panel"]["rows"], int(cov_selected["cumple_minimo"].sum())),
        row("Duplicados clave dimensional completa (DatosAnimales)", 0,
            int(dups[("DatosAnimales", "dimensiones + MGAP")])),
        row("Duplicados clave dimensional completa (DatosGenerales)", 0,
            int(dups[("DatosGenerales", "dimensiones + MGAP")])),
        row("Mortalidad ovina nula", 0, int(ovinos["AnimalesPorEspecieMortandadPD_AD"].isna().sum())),
        row("Mortalidad ovina negativa", 0, int((ovinos["AnimalesPorEspecieMortandadPD_AD"] < 0).sum())),
        row(f"Ovinos modelables {start}–{end} completos y no negativos", "sin errores",
            validates(filter_ovinos, animales)),
        row(f"DatosGenerales modelable {start}–{end} completo y no negativo", "sin errores",
            validates(filter_generales, generales)),
        row("Columnas MGAP 100 % nulas en 2016–2021", True,
            bool((mgap_null.loc[2016:2021] == 1).all())),
        row("Columnas MGAP completas desde 2022", True,
            bool((mgap_any_null.loc[2022:] == 0).all())),
        row(f"Cobertura mínima de las estaciones seleccionadas en {start}–{end}",
            f">= {cfg['climate']['minimum_coverage']}", float(cov_selected["cobertura"].min()),
            ok=cov_selected["cumple_minimo"].all()),
        row("Ejercicios con cobertura suficiente en estaciones excluidas",
            f"< {n_exercises}", int(cov_excluded["cumple_minimo"].sum()),
            ok=cov_excluded["cumple_minimo"].sum() < n_exercises),
        row("Duplicados estación–fecha en INIA", 0, int(dups[("INIA", "estación + fecha")])),
        row("Primera fecha INIA", exp["inia_first_date"], str(inia["Fecha"].min().date())),
        row("Última fecha INIA", exp["inia_last_date"], str(inia["Fecha"].max().date())),
    ]
    if not hashes.empty and hashes["sha256_registrado"].notna().any():
        rows.append(row("Archivos raw sin modificaciones (SHA-256)", True, bool(hashes["coincide"].all())))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Ejecución
# ---------------------------------------------------------------------------


def _md_table(df: pd.DataFrame) -> str:
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for values in df.itertuples(index=False):
        lines.append("| " + " | ".join("" if pd.isna(v) else str(v) for v in values) + " |")
    return "\n".join(lines)


def _exclusion_decisions(
    inia: pd.DataFrame, animales: pd.DataFrame, generales: pd.DataFrame, cfg: dict
) -> list[str]:
    catalog = load_catalogo(project_path(cfg["paths"]["catalogo_departamentos"]))
    unknown_dep = animales[~animales["DepartamentoCodigo"].isin(catalog["DepartamentoCodigo"])]
    masked = generales[generales[GENERALES_DECIMAL_COLUMNS].isna().any(axis=1)]
    masked_where = sorted(set(zip(masked["DepartamentoCodigo"], masked["Anio"])))
    negative = generales[generales[GENERALES_DECIMAL_COLUMNS].lt(0).any(axis=1)]
    negative_where = sorted(set(zip(negative["DepartamentoCodigo"], negative["Anio"])))
    wind = cfg["climate"]["columns"]["wind_run"]
    temp = cfg["climate"]["columns"]["temperature"]
    lines = []
    for station in cfg["excluded_stations"]:
        s = inia[inia[STATION_COLUMN] == nfc(station)]
        lines.append(
            f"- Estación **{station}** excluida: comienza el {s['Fecha'].min().date()} "
            f"y le falta {100 * s[wind].isna().mean():.1f} % de `{wind}`."
        )
    lines += [
        f"- Columnas {', '.join(f'`{c}`' for c in MGAP_COLUMNS)} excluidas: vacías en 2016–2021, "
        "no se imputan.",
        f"- {len(unknown_dep)} fila(s) de DatosAnimales con `DepartamentoCodigo` fuera del catálogo "
        f"(códigos {sorted(int(c) for c in unknown_dep['DepartamentoCodigo'].unique())}); "
        "quedan fuera por el filtro de departamentos.",
        f"- {len(masked)} fila(s) de DatosGenerales con `UnidadesGanaderas` o `SuperficieGanadera` "
        f"enmascarada como `********` (departamento, año: {[(int(d), int(y)) for d, y in masked_where]}). "
        "Se cargan como faltantes; el pipeline se detiene si alguna cae dentro del alcance modelable.",
        f"- {len(negative)} fila(s) de DatosGenerales con `UnidadesGanaderas` o `SuperficieGanadera` negativa "
        f"(departamento, año: {[(int(d), int(y)) for d, y in negative_where]}). Ninguna está en el período "
        f"{cfg['project']['start_year']}–{cfg['project']['end_year']}; el pipeline se detiene si aparece alguna.",
        f"- Ejercicio {cfg['project']['snig_years'][0]} excluido como observación principal: "
        "requiere clima desde julio del año anterior y INIA comienza en enero.",
        f"- Temperatura: se usa `{temp}`. `TMedia` difiere en promedio "
        f"{(inia['TMedia'] - inia[temp]).mean():.2f} °C y no se utiliza.",
        "- Los nombres de estación de INIA mezclan Unicode NFC y NFD; se normalizan a NFC antes del mapeo.",
    ]
    return lines


def run_audit(cfg: dict | None = None, out_dir: Path | None = None) -> dict[str, pd.DataFrame]:
    cfg = cfg or load_config()
    out_dir = out_dir or project_path(cfg["paths"]["audit_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    animales = load_animales(project_path(cfg["paths"]["raw_animales"]))
    generales = load_generales(project_path(cfg["paths"]["raw_generales"]))
    inia = load_inia(project_path(cfg["paths"]["raw_inia"]))

    loaded_rows = {
        cfg["paths"]["raw_animales"]: len(animales),
        cfg["paths"]["raw_generales"]: len(generales),
        cfg["paths"]["raw_inia"]: len(inia),
    }
    hashes = check_raw_hashes(cfg)
    inventory = pd.DataFrame(
        {
            "archivo": hashes["archivo"],
            "bytes": [(PROJECT_ROOT / a).stat().st_size for a in hashes["archivo"]],
            "filas": pd.array([loaded_rows.get(a) for a in hashes["archivo"]], dtype="Int64"),
            "sha256": hashes["sha256_actual"],
        }
    )
    coverage = climate_coverage(inia, cfg)

    tables = {
        "inventario": inventory,
        "verificacion_seccion9": section9_checks(animales, generales, inia, coverage, hashes, cfg),
        "esquema_DatosAnimales": schema_table(animales),
        "esquema_DatosGenerales": schema_table(generales),
        "esquema_INIA": schema_table(inia),
        "nulos_mgap_por_anio": mgap_null_by_year(animales, generales),
        "duplicados": duplicate_summary(animales, generales, inia),
        "valores_imposibles": impossible_values(animales, generales, inia, cfg),
        "faltantes_clima_por_estacion": climate_missing_by_station(inia, cfg),
        "cobertura_clima_estacion_ejercicio": coverage,
        "hashes_raw": hashes,
    }
    for name, table in tables.items():
        table.to_csv(out_dir / f"{name}.csv", index=False, encoding="utf-8")

    coverage_wide = (
        coverage.pivot(index=STATION_COLUMN, columns="AnioEjercicio", values="cobertura")
        .mul(100).round(1).reset_index()
    )
    checks = tables["verificacion_seccion9"]
    sections = [
        "# Auditoría de datos crudos",
        f"Generado: {datetime.now().isoformat(timespec='seconds')} · Python {platform.python_version()} · "
        f"pandas {metadata.version('pandas')} · numpy {metadata.version('numpy')}",
        "Archivo generado por `python -m src.data.audit`. No editar a mano.",
        f"## Verificación de la sección 9\n\n{int(checks['ok'].sum())} de {len(checks)} chequeos correctos.\n\n"
        + _md_table(checks),
        "## Inventario\n\n" + _md_table(inventory.drop(columns="sha256")),
        "## Columnas MGAP: % de nulos por año\n\n" + _md_table(tables["nulos_mgap_por_anio"]),
        "## Duplicados\n\n" + _md_table(tables["duplicados"]),
        "## Valores imposibles\n\n" + _md_table(tables["valores_imposibles"]),
        "## Faltantes climáticos por estación\n\n" + _md_table(tables["faltantes_clima_por_estacion"]),
        "## Cobertura climática por estación y ejercicio (%)\n\n"
        "Días con temperatura, precipitación y viento sobre los días del ejercicio julio–junio. "
        "Los ejercicios 2016 y 2026 son parciales por el rango del archivo.\n\n" + _md_table(coverage_wide),
        "## Decisiones de exclusión\n\n" + "\n".join(_exclusion_decisions(inia, animales, generales, cfg)),
        "Los esquemas completos por columna están en los CSV `esquema_*.csv` de esta carpeta.",
    ]
    (out_dir / "auditoria_datos.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")
    return tables


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--registrar-hashes", action="store_true", help="registra los SHA-256 de data/raw")
    args = parser.parse_args()
    cfg = load_config()
    if args.registrar_hashes:
        print(f"Manifiesto escrito en {write_hash_manifest(cfg)}")
        return
    checks = run_audit(cfg)["verificacion_seccion9"]
    print(checks.to_string(index=False))
    failed = checks[~checks["ok"]]
    if not failed.empty:
        raise SystemExit(f"{len(failed)} chequeo(s) de la sección 9 no coinciden")


if __name__ == "__main__":
    main()
