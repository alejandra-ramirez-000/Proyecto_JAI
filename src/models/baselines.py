"""Baselines obligatorios de regresión y clasificación (sección 17).

Cada baseline es una función `fit_predict(train, test)` que solo usa el
entrenamiento del fold (y, en persistencia, el rezago de la fila de prueba,
que es información del ejercicio anterior).

Uso:
    python -m src.models.baselines
"""

import numpy as np
import pandas as pd

from src.models.experiment import ModelSpec, run_and_write
from src.models.validation import DEPT, LABEL, LAG_LABEL


def department_mean(target: str):
    """R1: promedio histórico del departamento en los años de entrenamiento."""

    def fit_predict(train: pd.DataFrame, test: pd.DataFrame) -> np.ndarray:
        means = train.groupby(DEPT)[target].mean()
        return test[DEPT].map(means).to_numpy()

    return fit_predict


def persistence(lag_column: str):
    """R2: el valor del ejercicio anterior del mismo departamento."""

    def fit_predict(train: pd.DataFrame, test: pd.DataFrame) -> np.ndarray:
        return test[lag_column].to_numpy()

    return fit_predict


def majority_class(train: pd.DataFrame, test: pd.DataFrame):
    """C1: siempre la clase más frecuente del entrenamiento; probabilidad = prevalencia."""
    prevalence = train[LABEL].mean()
    predicted = int(prevalence > 0.5)
    return np.full(len(test), prevalence), np.full(len(test), predicted)


def risk_persistence(train: pd.DataFrame, test: pd.DataFrame):
    """C2: elevado si el ejercicio anterior del departamento superó el umbral del fold."""
    previous = test[LAG_LABEL].to_numpy()
    return previous, previous.astype(int)


def department_history(train: pd.DataFrame, test: pd.DataFrame):
    """C3: proporción histórica de años elevados del departamento; clase con corte 0,5."""
    proportions = train.groupby(DEPT)[LABEL].mean()
    proba = test[DEPT].map(proportions).to_numpy()
    return proba, (proba >= 0.5).astype(int)


REGRESSION_BASELINES = [
    ModelSpec("R1_promedio_departamental", department_mean("intensidad_ug_ha"), requires_lag=False, role="baseline"),
    ModelSpec("R2_persistencia", persistence("intensidad_lag1"), requires_lag=True, role="baseline"),
]

CLASSIFICATION_BASELINES = [
    ModelSpec("C1_clase_mayoritaria", majority_class, requires_lag=False, role="baseline"),
    ModelSpec("C2_persistencia_riesgo", risk_persistence, requires_lag=True, role="baseline"),
    ModelSpec("C3_historial_departamental", department_history, requires_lag=False, role="baseline"),
]


def main() -> None:
    run_dir = run_and_write("baselines", REGRESSION_BASELINES, CLASSIFICATION_BASELINES)
    print(f"Resultados en {run_dir}")


if __name__ == "__main__":
    main()
