"""Modelos de clasificación de mortalidad ovina elevada (sección 17.2).

Principal: regresión logística L2 con clima estandarizado y departamento
one-hot. Secundarios: logística Elastic Net y árbol de profundidad 1–2. El
bosque aleatorio restringido es solo sensibilidad (nunca única evidencia).

La logística Elastic Net no tiene grilla en la especificación: se fija
class_weight="balanced" y se exploran C y l1_ratio en una grilla mínima.
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from src.models.experiment import ModelSpec
from src.models.feature_sets import feature_specs
from src.models.regression import spec_role
from src.models.tuning import TunedModel

MORTALITY_TARGET = "tasa_mortalidad_1000"

# nombre: (estimador, grilla, rol)
MODELS = {
    "logistica": (
        LogisticRegression(max_iter=10_000),  # penalización L2 por defecto
        {"C": [0.01, 0.1, 0.3, 1, 3, 10], "class_weight": [None, "balanced"]},
        "principal",
    ),
    "logistica_en": (
        # saga recorre los datos en orden aleatorio: sin semilla, las predicciones cambian entre ejecuciones.
        LogisticRegression(solver="saga", max_iter=100_000, random_state=42),
        {"C": [0.1, 1, 10], "l1_ratio": [0.9, 0.5, 0.1], "class_weight": ["balanced"]},
        "secundario",
    ),
    "arbol": (
        DecisionTreeClassifier(random_state=42),
        {"class_weight": [None, "balanced"], "max_depth": [1, 2], "min_samples_leaf": [8, 6, 4]},
        "secundario",
    ),
    "bosque": (
        RandomForestClassifier(n_estimators=300, max_depth=2, min_samples_leaf=4,
                               class_weight="balanced", random_state=42),
        {},
        "sensibilidad",
    ),
}

CONTROL_MODEL = "logistica"


def classification_specs(quantile: float) -> list[ModelSpec]:
    specs = []
    for family, (estimator, grid, role) in MODELS.items():
        for fs in feature_specs(MORTALITY_TARGET):
            if fs["set"] == "H" and family != CONTROL_MODEL:
                continue
            model = TunedModel(estimator, grid, fs["numeric"], "classification", quantile=quantile)
            spec_role_name = "sensibilidad" if role == "sensibilidad" else spec_role(role, fs)
            specs.append(
                ModelSpec(f"{family}_{fs['set']}_{fs['window']}", model, fs["requires_lag"],
                          role=spec_role_name, family=family, feature_set=fs["set"], window=fs["window"])
            )
    return specs
