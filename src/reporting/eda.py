"""Análisis exploratorio (Entregable 3, sección 22).

Uso:
    python -m src.reporting.eda

Lee el panel y el clima diario generados por `python -m src.data.build_panel`
y escribe figuras en reports/figures/, tablas en reports/tables/ y el resumen
reports/eda.md. El punto 14 (observados frente a predicciones fuera de
muestra) se genera con los modelos en la Fase 5.
"""

from datetime import datetime

import pandas as pd

from src.config import PROJECT_ROOT, load_config, project_path
from src.features.build_features import FULL_WINDOW
from src.reporting import figures as fig
from src.reporting import tables as tab

SHORT_TARGETS = {"tasa_mortalidad_1000": "Mortalidad", "intensidad_ug_ha": "Intensidad"}


def load_inputs(cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    panel = pd.read_csv(project_path(cfg["paths"]["processed_dir"]) / "panel_departamento_ejercicio.csv")
    daily = pd.read_parquet(project_path(cfg["paths"]["interim_dir"]) / "clima_diario_con_ci.parquet")
    daily["ci_categoria"] = pd.Categorical(daily["ci_categoria"], categories=fig.CATEGORY_LABELS, ordered=True)
    return panel, daily


def run_eda(cfg: dict | None = None) -> dict[str, pd.DataFrame]:
    cfg = cfg or load_config()
    panel, daily = load_inputs(cfg)
    years = (cfg["project"]["start_year"], cfg["project"]["end_year"])
    figures_dir = project_path(cfg["paths"]["figures_dir"])
    tables_dir = project_path(cfg["paths"]["tables_dir"])
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    correlations = tab.correlation_table(panel)
    z = tab.zscores_by_department(panel, list(tab.TARGETS))
    tables = {
        "eda_cobertura_estacion_ejercicio": tab.coverage_by_station(daily),
        "eda_faltantes_estacion_anio": tab.missing_by_station_year(daily),
        "eda_dias_categoria_ci": tab.ci_category_days(daily, years),
        "eda_correlaciones": correlations,
        "eda_correlaciones_por_departamento": tab.per_department_correlations(panel),
        "eda_anios_extremos": tab.extreme_years(panel),
        "eda_comparacion_ventanas": tab.window_comparison(correlations),
    }
    for name, table in tables.items():
        table.to_csv(tables_dir / f"{name}.csv", index=False, encoding="utf-8")

    names = fig._department_names(panel)
    fx = f"_{FULL_WINDOW}"
    paths = {
        "01": fig.coverage_heatmap(tables["eda_cobertura_estacion_ejercicio"], years,
                                   figures_dir / "eda_01_cobertura_clima.png"),
        "02": fig.missing_heatmap(tables["eda_faltantes_estacion_anio"], figures_dir / "eda_02_faltantes_clima.png"),
        "03": fig.target_series(panel, "intensidad_ug_ha", "Intensidad ganadera por departamento (UG/ha)",
                                "Unidades ganaderas por hectárea ganadera", "{:.2f}",
                                figures_dir / "eda_03_intensidad_series.png"),
        "04": fig.target_series(panel, "tasa_mortalidad_1000", "Tasa proxy de mortalidad ovina por departamento (por mil)",
                                "Muertes por cada mil ovinos", "{:.0f}", figures_dir / "eda_04_mortalidad_series.png"),
        "05": fig.stock_and_deaths(panel, figures_dir / "eda_05_stock_y_muertes.png"),
        "06": fig.mortality_distribution(panel, figures_dir / "eda_06_mortalidad_distribucion.png"),
        "07": fig.ci_category_bars(tables["eda_dias_categoria_ci"], names, figures_dir / "eda_07_dias_categoria_ci.png"),
        "08": fig.scatter_by_department(panel, f"precip_total_mm{fx}", "tasa_mortalidad_1000",
                                        "Precipitación del ejercicio (mm)", "Mortalidad (por mil)",
                                        "Precipitación anual y mortalidad ovina", figures_dir / "eda_08_precip_vs_mortalidad.png"),
        "09": fig.scatter_by_department(panel, f"dias_ci_ge_1000{fx}", "tasa_mortalidad_1000",
                                        "Días con CI ≥ 1000", "Mortalidad (por mil)",
                                        "Días con CI ≥ 1000 y mortalidad ovina", figures_dir / "eda_09_ci1000_vs_mortalidad.png"),
        "10": fig.scatter_by_department(panel, f"dias_ci_ge_1200{fx}", "tasa_mortalidad_1000",
                                        "Días con CI ≥ 1200", "Mortalidad (por mil)",
                                        "Días con CI ≥ 1200 y mortalidad ovina", figures_dir / "eda_10_ci1200_vs_mortalidad.png"),
        "11": fig.correlation_heatmap(correlations, {**tab.CLIMATE_VARIABLES, **tab.LAG_VARIABLES}, SHORT_TARGETS,
                                      FULL_WINDOW, figures_dir / "eda_11_correlaciones.png"),
        "12": fig.zscore_heatmap(panel, z, "tasa_mortalidad_1000",
                                 "Años extremos de mortalidad ovina (z por departamento)",
                                 figures_dir / "eda_12_anios_extremos.png"),
        "13": fig.window_dot_plot(tables["eda_comparacion_ventanas"], tab.CLIMATE_VARIABLES, SHORT_TARGETS,
                                  figures_dir / "eda_13_ejercicio_vs_jul_oct.png"),
    }
    write_report(panel, tables, paths, cfg)
    return tables


def _top_correlations(correlations: pd.DataFrame, target: str, n: int = 5) -> pd.DataFrame:
    data = correlations[(correlations["objetivo"] == target) & (correlations["ventana"] == FULL_WINDOW)]
    data = data.reindex(data["r_intra_departamento"].abs().sort_values(ascending=False).index).head(n)
    return data.assign(variable=data["variable"].map(tab.CLIMATE_VARIABLES))[
        ["variable", "r_intra_departamento", "r_intra_departamento_y_anio", "r_global"]
    ].round(2)


def _md_table(df: pd.DataFrame) -> str:
    lines = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * df.shape[1]]
    lines += ["| " + " | ".join(map(str, row)) + " |" for row in df.itertuples(index=False)]
    return "\n".join(lines)


def write_report(panel: pd.DataFrame, tables: dict, paths: dict, cfg: dict) -> None:
    correlations = tables["eda_correlaciones"]
    climate = correlations[correlations["ventana"] == FULL_WINDOW]
    sign_flips = int((climate["r_global"] * climate["r_intra_departamento"] < 0).sum())
    lags = correlations[correlations["ventana"] == "historia"].set_index(["objetivo", "variable"])
    extremes = tables["eda_anios_extremos"]
    report_dir = project_path("reports")

    def image(key: str, caption: str) -> str:
        rel = paths[key].relative_to(report_dir).as_posix()
        return f"![{caption}]({rel})"

    sections = [
        "# Análisis exploratorio",
        f"Generado: {datetime.now().isoformat(timespec='seconds')} por `python -m src.reporting.eda`. No editar a mano; "
        "la interpretación va en `reports/eda_observaciones.md`.",
        "Este análisis describe los datos. No se usa para elegir variables ni modelos: los conjuntos A, B y C "
        "de la sección 13.6 ya están predefinidos.",
        "## Cifras clave",
        f"- Panel: {len(panel)} departamento–ejercicio, {panel['AnioEjercicio'].min()}–{panel['AnioEjercicio'].max()}.",
        f"- Correlación de la mortalidad con la del ejercicio anterior: global "
        f"{lags.loc[('tasa_mortalidad_1000', 'mortalidad_lag1'), 'r_global']:+.2f}, intra-departamento "
        f"{lags.loc[('tasa_mortalidad_1000', 'mortalidad_lag1'), 'r_intra_departamento']:+.2f} (n = 40).",
        f"- Correlación de la intensidad con la del ejercicio anterior: global "
        f"{lags.loc[('intensidad_ug_ha', 'intensidad_lag1'), 'r_global']:+.2f}, intra-departamento "
        f"{lags.loc[('intensidad_ug_ha', 'intensidad_lag1'), 'r_intra_departamento']:+.2f} (n = 40).",
        f"- {sign_flips} de {len(climate)} pares variable climática–objetivo cambian de signo entre la correlación "
        "global y la intra-departamento: la global mezcla diferencias entre regiones.",
        f"- {len(extremes)} departamento–ejercicio con |z| ≥ 1,5 en algún objetivo, en días con CI ≥ 1000 o en precipitación "
        "(tabla `reports/tables/eda_anios_extremos.csv`).",
        "### Variables climáticas con mayor |r| intra-departamento — mortalidad (ejercicio completo, n = 45)",
        _md_table(_top_correlations(correlations, "tasa_mortalidad_1000")),
        "### Variables climáticas con mayor |r| intra-departamento — intensidad (ejercicio completo, n = 45)",
        _md_table(_top_correlations(correlations, "intensidad_ug_ha")),
        "`r_intra_departamento_y_anio` descuenta además la media de cada ejercicio (shocks comunes a los cinco "
        "departamentos). Si cae mucho respecto de `r_intra_departamento`, la asociación viene de años que afectan "
        "a todos los departamentos a la vez, y la información efectiva se parece más a 9 años que a 45 observaciones.",
        "Con 45 observaciones, |r| < 0,29 no es distinguible de cero al 5 % (y menos aún tras comparar muchas variables).",
        "## 1. Cobertura por estación y ejercicio", image("01", "Cobertura climática"),
        "## 2. Faltantes de las variables climáticas requeridas", image("02", "Faltantes climáticos"),
        "## 3. Intensidad ganadera", image("03", "Intensidad por departamento"),
        "## 4. Mortalidad ovina por mil", image("04", "Mortalidad por departamento"),
        "## 5. Stock y muertes por separado", image("05", "Stock y muertes"),
        "## 6. Distribución de la mortalidad por departamento", image("06", "Distribución de mortalidad"),
        "## 7. Días por categoría de Chill Index", image("07", "Días por categoría de CI"),
        "## 8. Precipitación y mortalidad", image("08", "Precipitación y mortalidad"),
        "## 9. Días con CI ≥ 1000 y mortalidad", image("09", "CI 1000 y mortalidad"),
        "## 10. Días con CI ≥ 1200 y mortalidad", image("10", "CI 1200 y mortalidad"),
        "## 11. Correlaciones globales e intra-departamento", image("11", "Correlaciones"),
        "Por departamento (n = 9 cada uno): `reports/tables/eda_correlaciones_por_departamento.csv`.",
        "## 12. Años extremos", image("12", "Años extremos"),
        "## 13. Ejercicio completo frente a julio–octubre", image("13", "Comparación de ventanas"),
        "## 14. Observados frente a predicciones fuera de muestra",
    ]
    oos = sorted(project_path(cfg["paths"]["figures_dir"]).glob("eda_14_*.png"))
    if oos:
        sections.append("Generadas por `python -m src.models.run_models` (la corrida figura en el pie de cada imagen).")
        sections += [f"![{p.stem}]({p.relative_to(report_dir).as_posix()})" for p in oos]
    else:
        sections.append("Pendiente: se genera con `python -m src.models.run_models`.")
    (report_dir / "eda.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    run_eda()
    print(f"EDA escrito en {PROJECT_ROOT / 'reports'}")


if __name__ == "__main__":
    main()
