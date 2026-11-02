"""Ejecución de experimentos: corre modelos con Leave-One-Year-Out, resume métricas y guarda la corrida.

Cada corrida se guarda en `reports/runs/<fecha-hora>_<nombre>/` y nunca
sobrescribe una anterior (sección 28). La carpeta contiene predicciones fuera
de muestra, métricas globales, por departamento y por año, hiperparámetros y
coeficientes por fold, y los metadatos.
"""

import hashlib
import json
import platform
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from importlib import metadata
from pathlib import Path

import pandas as pd
from joblib import Parallel, delayed

from src.config import load_config, project_path
from src.data.audit import compute_raw_hashes
from src.models.validation import (
    EVALUATION_SETS,
    YEAR,
    balanced_accuracy_stat,
    classification_metrics,
    cross_validate_classification,
    cross_validate_regression,
    evaluation_set,
    mae_skill,
    mae_stat,
    mean_fold_auc,
    metrics_by,
    regression_metrics,
    roc_auc_stat,
    year_block_bootstrap,
)
from src.reporting.markdown import md_table

REGRESSION_TARGET = "intensidad_ug_ha"
ROLES = ["baseline", "principal", "control", "secundario", "sensibilidad"]


@dataclass(frozen=True)
class ModelSpec:
    name: str
    fit_predict: Callable
    requires_lag: bool
    role: str = "principal"
    family: str = ""
    feature_set: str = ""
    window: str = ""

    @property
    def baseline(self) -> bool:
        return self.role == "baseline"


def load_panel(cfg: dict) -> pd.DataFrame:
    return pd.read_csv(project_path(cfg["paths"]["processed_dir"]) / "panel_departamento_ejercicio.csv")


def _sets_for(spec: ModelSpec):
    for set_name, with_lag in EVALUATION_SETS.items():
        if spec.requires_lag and not with_lag:
            continue
        yield set_name, with_lag


def _spec_columns(spec: ModelSpec, set_name: str) -> dict:
    return {"conjunto": set_name, "rol": spec.role, "familia": spec.family,
            "conjunto_variables": spec.feature_set, "ventana": spec.window}


def _run_one(spec: ModelSpec, set_name: str, with_lag: bool, panel: pd.DataFrame,
             cross_validate: Callable) -> tuple[pd.DataFrame, list[dict]]:
    """Una especificación en un conjunto. Devuelve los registros porque en paralelo
    el modelo vive en otro proceso y sus `records` no vuelven solos."""
    if hasattr(spec.fit_predict, "reset"):
        spec.fit_predict.reset()
    oof = cross_validate(evaluation_set(panel, with_lag), spec)
    records = [{"modelo": spec.name, "conjunto": set_name, **r} for r in getattr(spec.fit_predict, "records", [])]
    return oof.assign(**_spec_columns(spec, set_name)), records


def _run(panel: pd.DataFrame, specs: list[ModelSpec], cross_validate: Callable,
         n_jobs: int = 1) -> tuple[pd.DataFrame, list[dict]]:
    jobs = [(spec, set_name, with_lag) for spec in specs for set_name, with_lag in _sets_for(spec)]
    results = Parallel(n_jobs=n_jobs)(
        delayed(_run_one)(spec, set_name, with_lag, panel, cross_validate) for spec, set_name, with_lag in jobs
    )
    parts = [oof for oof, _ in results]
    records = [record for _, recs in results for record in recs]
    return pd.concat(parts, ignore_index=True), records


def run_regression(panel: pd.DataFrame, specs: list[ModelSpec], n_jobs: int = 1) -> tuple[pd.DataFrame, list[dict]]:
    return _run(panel, specs,
                lambda data, spec: cross_validate_regression(data, spec.fit_predict, REGRESSION_TARGET, spec.name),
                n_jobs)


def run_classification(panel: pd.DataFrame, specs: list[ModelSpec], quantile: float,
                       n_jobs: int = 1) -> tuple[pd.DataFrame, list[dict]]:
    return _run(panel, specs,
                lambda data, spec: cross_validate_classification(data, spec.fit_predict, spec.name, quantile),
                n_jobs)


def _groups(oof: pd.DataFrame):
    return oof.groupby(["conjunto", "modelo"], sort=False)


def _spec_info(group: pd.DataFrame) -> dict:
    first = group.iloc[0]
    return {c: first[c] for c in ["rol", "familia", "conjunto_variables", "ventana"]}


def summarize_regression(oof: pd.DataFrame, cfg: dict) -> dict[str, pd.DataFrame]:
    n_boot, seed = cfg["validation"]["bootstrap_samples"], cfg["project"]["random_seed"]
    rows = []
    for (set_name, model), group in _groups(oof):
        mae_ci = year_block_bootstrap(group, mae_stat, ["y_true", "y_pred"], n_boot, seed)
        rows.append({"conjunto": set_name, "modelo": model, **_spec_info(group), **regression_metrics(group),
                     "MAE_ic95_inf": mae_ci["ic95_inf"], "MAE_ic95_sup": mae_ci["ic95_sup"]})
    summary = pd.DataFrame(rows)

    # Skill de MAE frente a cada baseline evaluado en el mismo conjunto.
    baselines = summary[summary["rol"] == "baseline"]
    for baseline in baselines["modelo"].unique():
        reference = baselines[baselines["modelo"] == baseline].set_index("conjunto")["MAE"]
        summary[f"skill_vs_{baseline}"] = [
            mae_skill(mae, reference[c]) if c in reference.index else float("nan")
            for c, mae in zip(summary["conjunto"], summary["MAE"])
        ]
    return {
        "regresion_metricas": summary,
        "regresion_por_departamento": _by(oof, regression_metrics, "Departamento"),
        "regresion_por_anio": _by(oof, regression_metrics, YEAR),
    }


def summarize_classification(oof: pd.DataFrame, cfg: dict) -> dict[str, pd.DataFrame]:
    n_boot, seed = cfg["validation"]["bootstrap_samples"], cfg["project"]["random_seed"]
    rows = []
    for (set_name, model), group in _groups(oof):
        ba_ci = year_block_bootstrap(group, balanced_accuracy_stat, ["y_true", "y_pred"], n_boot, seed)
        auc_ci = year_block_bootstrap(group, roc_auc_stat, ["y_true", "y_proba"], n_boot, seed)
        rows.append({"conjunto": set_name, "modelo": model, **_spec_info(group), **classification_metrics(group),
                     **mean_fold_auc(group),
                     "balanced_accuracy_ic95_inf": ba_ci["ic95_inf"], "balanced_accuracy_ic95_sup": ba_ci["ic95_sup"],
                     "roc_auc_ic95_inf": auc_ci["ic95_inf"], "roc_auc_ic95_sup": auc_ci["ic95_sup"]})
    return {
        "clasificacion_metricas": pd.DataFrame(rows),
        "clasificacion_por_departamento": _by(oof, classification_metrics, "Departamento"),
        "clasificacion_por_anio": _by(oof, classification_metrics, YEAR),
    }


def _by(oof: pd.DataFrame, metric_fn, by: str) -> pd.DataFrame:
    parts = []
    for (set_name, model), group in _groups(oof):
        parts.append(metrics_by(group, metric_fn, by).assign(conjunto=set_name, modelo=model))
    out = pd.concat(parts, ignore_index=True)
    return out[["conjunto", "modelo"] + [c for c in out.columns if c not in ("conjunto", "modelo")]]


def records_tables(records: list[dict], prefix: str) -> dict[str, pd.DataFrame]:
    """Hiperparámetros elegidos y coeficientes por fold (secciones 23 y 28)."""
    if not records:
        return {}
    params = pd.DataFrame(
        [{"modelo": r["modelo"], "conjunto": r["conjunto"], "fold": r["fold"],
          "hiperparametros": json.dumps(r["hiperparametros"], sort_keys=True), "puntaje_interno": r["puntaje_interno"]}
         for r in records]
    )
    coefs = pd.DataFrame(
        [{"modelo": r["modelo"], "conjunto": r["conjunto"], "fold": r["fold"], "variable": name, "valor": value}
         for r in records for name, value in r["coeficientes"].items()]
    )
    return {f"{prefix}_hiperparametros": params, f"{prefix}_coeficientes": coefs}


# ---------------------------------------------------------------------------
# Escritura de la corrida
# ---------------------------------------------------------------------------


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_metadata(cfg: dict, name: str, panel: pd.DataFrame, specs: dict[str, list[ModelSpec]]) -> dict:
    panel_path = project_path(cfg["paths"]["processed_dir"]) / "panel_departamento_ejercicio.csv"
    folds = {
        set_name: sorted(int(y) for y in evaluation_set(panel, with_lag)[YEAR].unique())
        for set_name, with_lag in EVALUATION_SETS.items()
    }
    models = {
        task: [{"nombre": s.name, "rol": s.role, "requiere_rezago": s.requires_lag,
                "variables": getattr(s.fit_predict, "numeric", None),
                "grilla": getattr(s.fit_predict, "grid", None)} for s in task_specs]
        for task, task_specs in specs.items()
    }
    return {
        "corrida": name,
        "generado": datetime.now().isoformat(timespec="seconds"),
        "python": platform.python_version(),
        "paquetes": {p: metadata.version(p) for p in ["pandas", "numpy", "scikit-learn"]},
        "semilla": cfg["project"]["random_seed"],
        "panel_sha256": _file_sha256(panel_path),
        "raw_sha256": compute_raw_hashes(cfg),
        "folds_por_conjunto": folds,
        "modelos": models,
        "configuracion": cfg,
    }


def _summary_markdown(name: str, tables: dict[str, pd.DataFrame], note: str | None = None) -> str:
    reg = tables["regresion_metricas"]
    cls = tables["clasificacion_metricas"]
    reg = reg[reg["rol"].isin(["baseline", "principal", "control"])]
    cls = cls[cls["rol"].isin(["baseline", "principal", "control"])]
    skill_cols = [c for c in reg.columns if c.startswith("skill_vs_")]
    sections = [f"# Corrida `{name}`"]
    if note:
        sections.append(f"> **Nota:** {note}")
    sections += [
        "Métricas fuera de muestra (Leave-One-Year-Out). Conjunto `completo`: 45 filas, 9 folds. "
        "Conjunto `con_rezago`: 40 filas (2018–2025), 8 folds. IC 95 %: bootstrap por bloques de ejercicio.",
        "Se muestran baselines, modelos principales y controles. Secundarios y sensibilidad (julio–octubre, "
        "bosque) están en los CSV de métricas.",
    ]
    if "criterios_regresion" in tables:
        sections += ["## Criterios de la sección 20", "### Regresión", md_table(tables["criterios_regresion"]),
                     "### Clasificación", md_table(tables["criterios_clasificacion"])]
    sections += [
        "## Regresión: intensidad ganadera (UG/ha)",
        md_table(reg[["conjunto", "modelo", "rol", "n", "MAE", "MAE_ic95_inf", "MAE_ic95_sup", "RMSE", "R2"]
                     + skill_cols], "{:.4f}"),
        "## Clasificación: mortalidad ovina elevada",
        md_table(cls[["conjunto", "modelo", "rol", "n", "prevalencia", "balanced_accuracy", "balanced_accuracy_ic95_inf",
                      "balanced_accuracy_ic95_sup", "roc_auc", "roc_auc_promedio_folds", "average_precision",
                      "recall", "especificidad",
                      "brier", "tn", "fp", "fn", "tp"]]),
        "Detalle por departamento y por ejercicio en los CSV `*_por_departamento.csv` y `*_por_anio.csv`; "
        "hiperparámetros y coeficientes por fold en `*_hiperparametros.csv` y `*_coeficientes.csv`.",
    ]
    return "\n\n".join(sections) + "\n"


def write_run(name: str, tables: dict[str, pd.DataFrame], meta: dict, cfg: dict, note: str | None = None) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = project_path(cfg["paths"]["runs_dir"]) / f"{stamp}_{name}"
    run_dir.mkdir(parents=True, exist_ok=False)
    for table_name, table in tables.items():
        table.to_csv(run_dir / f"{table_name}.csv", index=False, encoding="utf-8")
    if note:
        meta = {**meta, "nota": note}
    (run_dir / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    (run_dir / "resumen.md").write_text(_summary_markdown(name, tables, note), encoding="utf-8")
    return run_dir


def run_experiment(regression_specs: list[ModelSpec], classification_specs: list[ModelSpec],
                   cfg: dict) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Corre todos los modelos y devuelve las tablas de resultados y el panel usado."""
    panel = load_panel(cfg)
    n_jobs = cfg["validation"]["n_jobs"]
    reg_oof, reg_records = run_regression(panel, regression_specs, n_jobs)
    cls_oof, cls_records = run_classification(panel, classification_specs, cfg["targets"]["high_mortality_quantile"],
                                              n_jobs)
    tables = {
        "regresion_predicciones": reg_oof,
        "clasificacion_predicciones": cls_oof,
        **summarize_regression(reg_oof, cfg),
        **summarize_classification(cls_oof, cfg),
        **records_tables(reg_records, "regresion"),
        **records_tables(cls_records, "clasificacion"),
    }
    return tables, panel


def run_and_write(name: str, regression_specs: list[ModelSpec], classification_specs: list[ModelSpec],
                  cfg: dict | None = None) -> Path:
    cfg = cfg or load_config()
    tables, panel = run_experiment(regression_specs, classification_specs, cfg)
    meta = run_metadata(cfg, name, panel, {"regresion": regression_specs, "clasificacion": classification_specs})
    return write_run(name, tables, meta, cfg)
