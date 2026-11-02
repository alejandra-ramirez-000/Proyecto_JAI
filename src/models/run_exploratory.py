"""Ronda exploratoria registrada: modelos principales y controles con hiperparámetros fijos.

Uso:
    python -m src.models.run_exploratory

Motivo y registro (secciones 13.6, 17.1 y 18.2): en la corrida
`20261030-092748_modelos` la selección interna de hiperparámetros empató en
balanced accuracy 0,5 en varios folds y eligió la opción más regularizada,
con probabilidades casi constantes. La sección 18.2 contempla "fijar un
hiperparámetro razonable" cuando el entrenamiento interno es demasiado
pequeño. Como esta decisión se toma después de ver los resultados, la ronda es
EXPLORATORIA: sus métricas no reemplazan a las de la corrida registrada y no
pueden presentarse como evaluación no sesgada.

Valores fijos:
- Ridge: alpha = 1 (valor central de la grilla de la sección 17.1).
- Logística L2: C = 1 y class_weight = "balanced" (valor por defecto de
  scikit-learn y ponderación sugerida en la sección 17.2 ante desbalance).

Se corren solo las familias principales (Ridge y logística) con todos sus
conjuntos de variables y ventanas, más los baselines para los criterios.
"""

from dataclasses import replace

from src.config import load_config
from src.models.assessment import classification_criteria, regression_criteria
from src.models.baselines import CLASSIFICATION_BASELINES, REGRESSION_BASELINES
from src.models.classification import classification_specs
from src.models.experiment import ModelSpec, run_experiment, run_metadata, write_run
from src.models.feature_sets import TARGET_LAGS
from src.models.regression import regression_specs

RUN_NAME = "exploratoria_hiperparametros_fijos"
REFERENCE_RUN = "20261030-092748_modelos"
FIXED_GRIDS = {
    "ridge": {"alpha": [1.0]},
    "logistica": {"C": [1.0], "class_weight": ["balanced"]},
}
NOTE = (
    f"Ronda EXPLORATORIA definida después de ver la corrida {REFERENCE_RUN}. Hiperparámetros fijos "
    f"(Ridge alpha=1; logística C=1, class_weight='balanced'). No reemplaza a la corrida registrada "
    "ni constituye una evaluación no sesgada."
)


def fixed(specs: list[ModelSpec]) -> list[ModelSpec]:
    """Copias de las especificaciones de las familias principales con grilla de un solo valor."""
    out = []
    for spec in specs:
        if spec.family not in FIXED_GRIDS:
            continue
        model = replace(spec.fit_predict, grid=FIXED_GRIDS[spec.family], records=[])
        out.append(replace(spec, name=f"{spec.name}_fijo", fit_predict=model))
    return out


def main() -> None:
    cfg = load_config()
    reg_specs = REGRESSION_BASELINES + fixed(regression_specs())
    cls_specs = CLASSIFICATION_BASELINES + fixed(classification_specs(cfg["targets"]["high_mortality_quantile"]))
    tables, panel = run_experiment(reg_specs, cls_specs, cfg)
    lags = set(TARGET_LAGS.values())
    tables["criterios_regresion"] = regression_criteria(tables, cfg, lags)
    tables["criterios_clasificacion"] = classification_criteria(tables, cfg, lags)

    meta = run_metadata(cfg, RUN_NAME, panel, {"regresion": reg_specs, "clasificacion": cls_specs})
    meta["exploratoria"] = {"corrida_de_referencia": REFERENCE_RUN, "grillas_fijas": FIXED_GRIDS}
    run_dir = write_run(RUN_NAME, tables, meta, cfg, note=NOTE)
    print(f"Resultados en {run_dir}")


if __name__ == "__main__":
    main()
