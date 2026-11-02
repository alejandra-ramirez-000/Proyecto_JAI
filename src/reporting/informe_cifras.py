"""Cifras del informe final, cada una leída de un artefacto guardado (sección 30, Fase 6).

Uso:
    python -m src.reporting.informe_cifras

Escribe `reports/tables/informe_cifras.csv` con identificador, descripción,
valor y archivo de origen. El informe final cita estas cifras; un test verifica
que se regeneran idénticas desde los artefactos.
"""

import pandas as pd

from src.config import load_config, project_path

RUN_MODELS = "20261030-103735_modelos"
RUN_V10 = "20261030-092748_modelos"
RUN_EXPLORATORY = "20261030-102307_exploratoria_hiperparametros_fijos"


class Cifras:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.rows: list[dict] = []
        self._cache: dict[str, pd.DataFrame] = {}

    def read(self, relative: str) -> pd.DataFrame:
        if relative not in self._cache:
            path = project_path(relative)
            self._cache[relative] = pd.read_parquet(path) if relative.endswith(".parquet") else pd.read_csv(path)
        return self._cache[relative]

    def add(self, key: str, description: str, value, source: str) -> None:
        if hasattr(value, "item"):
            value = value.item()
        self.rows.append({"id": key, "descripcion": description, "valor": value, "fuente": source})

    def metric(self, run: str, table: str, set_name: str, model: str, column: str):
        source = f"reports/runs/{run}/{table}.csv"
        df = self.read(source)
        row = df[(df["conjunto"] == set_name) & (df["modelo"] == model)]
        if len(row) != 1:
            raise KeyError(f"{source}: {set_name}/{model} no encontrado")
        return row[column].iloc[0], source

    def add_metric(self, key: str, description: str, run: str, table: str, set_name: str, model: str, column: str):
        value, source = self.metric(run, table, set_name, model, column)
        self.add(key, description, value, f"{source} [{set_name}, {model}, {column}]")

    def frame(self) -> pd.DataFrame:
        return pd.DataFrame(self.rows)


def _data_figures(c: Cifras) -> None:
    panel_src = "data/processed/panel_departamento_ejercicio.csv"
    panel = c.read(panel_src)
    lagged = panel.dropna(subset=["intensidad_lag1", "mortalidad_lag1"])
    c.add("panel_filas", "Filas del panel departamento–ejercicio", len(panel), panel_src)
    c.add("panel_filas_rezago", "Filas del panel con rezago", len(lagged), panel_src)
    for col, name in [("intensidad_ug_ha", "intensidad"), ("tasa_mortalidad_1000", "mortalidad")]:
        c.add(f"{name}_min", f"Mínimo de {col}", round(panel[col].min(), 3), panel_src)
        c.add(f"{name}_max", f"Máximo de {col}", round(panel[col].max(), 3), panel_src)
    medians = panel.groupby("Departamento")["tasa_mortalidad_1000"].median()
    for dept in ["Salto", "Canelones"]:
        c.add(f"mortalidad_mediana_{dept.lower()}", f"Mediana de mortalidad por mil en {dept}",
              round(medians[dept], 1), panel_src)
    c.add("cobertura_min_ejercicio", "Cobertura climática mínima, ejercicio completo",
          round(panel["cobertura_ejercicio"].min(), 4), panel_src)
    c.add("cobertura_min_jul_oct", "Cobertura climática mínima, julio–octubre",
          round(panel["cobertura_jul_oct"].min(), 4), panel_src)
    precip = panel.groupby("AnioEjercicio")["precip_total_mm_ejercicio"].mean()
    c.add("precip_media_2023", "Precipitación media de los cinco departamentos, ejercicio 2023 (mm)",
          round(precip[2023], 0), panel_src)
    c.add("precip_media_2023_es_minima", "2023 es el ejercicio de menor precipitación media", bool(precip.idxmin() == 2023),
          panel_src)

    coverage_src = "reports/tables/eda_cobertura_estacion_ejercicio.csv"
    coverage = c.read(coverage_src)
    c.add("dias_sin_ci", "Días sin Chill Index calculable (cinco estaciones, todo el archivo)",
          int((coverage["dias_con_registro"] - coverage["dias_validos"]).sum()), coverage_src)

    audit_src = "reports/auditoria/verificacion_seccion9.csv"
    checks = c.read(audit_src)
    c.add("auditoria_chequeos_ok", "Chequeos de la sección 9 que coinciden", int(checks["ok"].sum()), audit_src)
    c.add("auditoria_chequeos_total", "Chequeos de la sección 9", len(checks), audit_src)
    ovinos = checks.loc[checks["chequeo"] == "Filas ovinas en los 5 departamentos", "observado"].iloc[0]
    c.add("filas_ovinas_alcance", "Filas ovinas originales en los cinco departamentos", int(ovinos), audit_src)
    impossible_src = "reports/auditoria/valores_imposibles.csv"
    impossible = c.read(impossible_src)
    negatives = impossible.loc[impossible["columna"] == "SuperficieGanadera", "violaciones"].iloc[0]
    c.add("superficie_negativa_filas", "Filas con SuperficieGanadera negativa (todas de 2016)", int(negatives),
          impossible_src)
    schema_src = "reports/auditoria/esquema_DatosGenerales.csv"
    schema = c.read(schema_src)
    masked = schema.loc[schema["columna"] == "SuperficieGanadera", "nulos"].iloc[0]
    c.add("superficie_enmascarada_filas", "Filas con SuperficieGanadera enmascarada (********)", int(masked), schema_src)


def _correlations(c: Cifras) -> None:
    src = "reports/tables/eda_correlaciones.csv"
    corr = c.read(src)

    def add(key, target, column, field, description):
        row = corr[(corr["objetivo"] == target) & (corr["columna"] == column)]
        c.add(key, description, round(row[field].iloc[0], 2), f"{src} [{target}, {column}, {field}]")

    mort, inten = "tasa_mortalidad_1000", "intensidad_ug_ha"
    add("r_mort_lag_global", mort, "mortalidad_lag1", "r_global", "r mortalidad vs. mortalidad del año anterior, global")
    add("r_mort_lag_intra", mort, "mortalidad_lag1", "r_intra_departamento",
        "r mortalidad vs. mortalidad del año anterior, intra-departamento")
    add("r_int_lag_global", inten, "intensidad_lag1", "r_global", "r intensidad vs. intensidad del año anterior, global")
    add("r_int_lag_intra", inten, "intensidad_lag1", "r_intra_departamento",
        "r intensidad vs. intensidad del año anterior, intra-departamento")
    for var, label in [("dias_ci_ge_1000_ejercicio", "ci1000"), ("dias_ci_ge_1200_ejercicio", "ci1200"),
                       ("precip_total_mm_ejercicio", "precip"), ("temp_media_c_ejercicio", "temp")]:
        add(f"r_mort_{label}_global", mort, var, "r_global", f"r mortalidad vs. {var}, global")
        add(f"r_mort_{label}_intra", mort, var, "r_intra_departamento", f"r mortalidad vs. {var}, intra-departamento")
        add(f"r_mort_{label}_intra_anio", mort, var, "r_intra_departamento_y_anio",
            f"r mortalidad vs. {var}, intra-departamento y año")


def _models(c: Cifras) -> None:
    reg, cls = "regresion_metricas", "clasificacion_metricas"
    for model, set_name, key in [
        ("R1_promedio_departamental", "completo", "R1_completo"),
        ("R1_promedio_departamental", "con_rezago", "R1_rezago"),
        ("R2_persistencia", "con_rezago", "R2"),
        ("ridge_A_ejercicio", "completo", "ridge_A_completo"),
        ("ridge_B_ejercicio", "completo", "ridge_B_completo"),
        ("ridge_A_ejercicio", "con_rezago", "ridge_A_rezago"),
        ("ridge_B_ejercicio", "con_rezago", "ridge_B_rezago"),
        ("ridge_H_sin_clima", "con_rezago", "ridge_H"),
        ("ridge_C-A_ejercicio", "con_rezago", "ridge_CA"),
        ("ridge_C-B_ejercicio", "con_rezago", "ridge_CB"),
    ]:
        for column in ["MAE", "MAE_ic95_inf", "MAE_ic95_sup"]:
            c.add_metric(f"{key}_{column}", f"{column} de {model} ({set_name})", RUN_MODELS, reg, set_name, model, column)
    criteria = "criterios_regresion"
    for model, key in [("ridge_H_sin_clima", "ridge_H"), ("ridge_C-A_ejercicio", "ridge_CA"),
                       ("ridge_C-B_ejercicio", "ridge_CB")]:
        c.add_metric(f"{key}_skill_mejor_baseline", f"Skill de MAE de {model} frente al mejor baseline",
                     RUN_MODELS, criteria, "con_rezago", model, "skill_vs_mejor_baseline")
        c.add_metric(f"{key}_skill_control", f"Skill de MAE de {model} frente al control sin clima",
                     RUN_MODELS, criteria, "con_rezago", model, "skill_vs_control_sin_clima")
    c.add_metric("ridge_H_skill_min_sin_anio", "Skill mínimo del control H al quitar un ejercicio",
                 RUN_MODELS, criteria, "con_rezago", "ridge_H_sin_clima", "skill_minimo_sin_un_anio")

    for model, set_name, key in [
        ("C2_persistencia_riesgo", "con_rezago", "C2"),
        ("C1_clase_mayoritaria", "completo", "C1_completo"),
        ("logistica_H_sin_clima", "con_rezago", "log_H"),
        ("logistica_A_ejercicio", "completo", "log_A_completo"),
        ("logistica_A_ejercicio", "con_rezago", "log_A_rezago"),
        ("logistica_B_ejercicio", "completo", "log_B_completo"),
        ("logistica_B_ejercicio", "con_rezago", "log_B_rezago"),
        ("logistica_C-A_ejercicio", "con_rezago", "log_CA"),
        ("logistica_C-B_ejercicio", "con_rezago", "log_CB"),
    ]:
        for column in ["balanced_accuracy", "balanced_accuracy_ic95_inf", "balanced_accuracy_ic95_sup",
                       "roc_auc", "roc_auc_promedio_folds", "prevalencia"]:
            c.add_metric(f"{key}_{column}", f"{column} de {model} ({set_name})", RUN_MODELS, cls, set_name, model, column)
    c.add_metric("log_H_v10_balanced_accuracy", "BA del control H con el criterio v1.0", RUN_V10, cls,
                 "con_rezago", "logistica_H_sin_clima", "balanced_accuracy")
    c.add_metric("log_H_fijo_balanced_accuracy", "BA del control H con C fijo (exploratoria)", RUN_EXPLORATORY, cls,
                 "con_rezago", "logistica_H_sin_clima_fijo", "balanced_accuracy")
    c.add_metric("log_A_completo_dif_min_sin_anio", "Diferencia mínima de BA de logística A (completo) al quitar un año",
                 RUN_MODELS, "criterios_clasificacion", "completo", "logistica_A_ejercicio", "diferencia_minima_sin_un_anio")

    source = f"reports/runs/{RUN_MODELS}/{cls}.csv"
    metrics = c.read(source)
    for set_name in ["completo", "con_rezago"]:
        subset = metrics[metrics["conjunto"] == set_name]
        c.add(f"brier_min_baseline_{set_name}", f"Brier mínimo de los baselines ({set_name})",
              round(subset.loc[subset["rol"] == "baseline", "brier"].min(), 3), source)
        c.add(f"brier_min_modelos_{set_name}", f"Brier mínimo de los modelos no baseline ({set_name})",
              round(subset.loc[subset["rol"] != "baseline", "brier"].min(), 3), source)
    n_specs = metrics.loc[metrics["rol"] != "baseline", "modelo"].nunique()
    reg_specs = c.read(f"reports/runs/{RUN_MODELS}/{reg}.csv")
    c.add("especificaciones_evaluadas", "Especificaciones no baseline evaluadas (regresión + clasificación)",
          int(n_specs + reg_specs.loc[reg_specs["rol"] != "baseline", "modelo"].nunique()), source)
    for task in ["regresion", "clasificacion"]:
        crit_src = f"reports/runs/{RUN_MODELS}/criterios_{task}.csv"
        crit = c.read(crit_src)
        c.add(f"{task}_principales_con_valor", f"Modelos principales con valor predictivo ({task})",
              int((crit["valor_predictivo"] == "sí").sum()), crit_src)


def collect(cfg: dict | None = None) -> pd.DataFrame:
    c = Cifras(cfg or load_config())
    _data_figures(c)
    _correlations(c)
    _models(c)
    return c.frame()


def main() -> None:
    cfg = load_config()
    out = project_path(cfg["paths"]["tables_dir"]) / "informe_cifras.csv"
    collect(cfg).to_csv(out, index=False, encoding="utf-8")
    print(f"Cifras escritas en {out}")


if __name__ == "__main__":
    main()
