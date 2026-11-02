"""Corre baselines y modelos en una misma corrida y evalúa los criterios de la sección 20.

Uso:
    python -m src.models.run_models
"""

import shutil

from src.config import load_config, project_path
from src.models.assessment import classification_criteria, regression_criteria
from src.models.baselines import CLASSIFICATION_BASELINES, REGRESSION_BASELINES
from src.models.classification import classification_specs
from src.models.experiment import run_experiment, run_metadata, write_run
from src.models.feature_sets import TARGET_LAGS
from src.models.regression import regression_specs
from src.reporting import figures

RUN_NAME = "modelos"


def main() -> None:
    cfg = load_config()
    reg_specs = REGRESSION_BASELINES + regression_specs()
    cls_specs = CLASSIFICATION_BASELINES + classification_specs(cfg["targets"]["high_mortality_quantile"])
    tables, panel = run_experiment(reg_specs, cls_specs, cfg)
    lags = set(TARGET_LAGS.values())
    tables["criterios_regresion"] = regression_criteria(tables, cfg, lags)
    tables["criterios_clasificacion"] = classification_criteria(tables, cfg, lags)

    meta = run_metadata(cfg, RUN_NAME, panel, {"regresion": reg_specs, "clasificacion": cls_specs})
    run_dir = write_run(RUN_NAME, tables, meta, cfg)

    figure_paths = figures.out_of_sample_figures(tables, run_dir, run_dir.name)
    figures_dir = project_path(cfg["paths"]["figures_dir"])
    for path in figure_paths:
        shutil.copy(path, figures_dir / path.name)
    print(f"Resultados en {run_dir}")


if __name__ == "__main__":
    main()
