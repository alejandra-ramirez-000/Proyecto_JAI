"""Modelos de regresión de la intensidad ganadera (sección 17.1).

Principal: Ridge con clima estandarizado y departamento one-hot. Secundarios:
regresión lineal, Elastic Net y árbol poco profundo. Las grillas son las de la
especificación, ordenadas de más a menos regularizado.
"""

from sklearn.linear_model import ElasticNet, LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor

from src.features.build_features import SENSITIVE_WINDOW
from src.models.experiment import REGRESSION_TARGET, ModelSpec
from src.models.feature_sets import feature_specs
from src.models.tuning import TunedModel

# nombre: (estimador, grilla, rol, drop_first en el one-hot)
MODELS = {
    "ridge": (Ridge(), {"alpha": [100, 30, 10, 3, 1, 0.1]}, "principal", False),
    "lineal": (LinearRegression(), {}, "secundario", True),
    "elasticnet": (
        ElasticNet(max_iter=100_000),
        {"alpha": [10, 1, 0.1, 0.01], "l1_ratio": [0.9, 0.5, 0.1]},
        "secundario",
        False,
    ),
    "arbol": (
        DecisionTreeRegressor(random_state=42),
        {"max_depth": [1, 2], "min_samples_leaf": [8, 6, 4]},
        "secundario",
        False,
    ),
}

CONTROL_MODEL = "ridge"


def spec_role(family_role: str, feature_spec: dict) -> str:
    if feature_spec["set"] == "H":
        return "control"
    if feature_spec["window"] == SENSITIVE_WINDOW:
        return "sensibilidad"
    return family_role


def regression_specs() -> list[ModelSpec]:
    specs = []
    for family, (estimator, grid, role, drop_first) in MODELS.items():
        for fs in feature_specs(REGRESSION_TARGET):
            if fs["set"] == "H" and family != CONTROL_MODEL:
                continue
            model = TunedModel(estimator, grid, fs["numeric"], "regression",
                               target=REGRESSION_TARGET, drop_first=drop_first)
            specs.append(
                ModelSpec(f"{family}_{fs['set']}_{fs['window']}", model, fs["requires_lag"],
                          role=spec_role(role, fs), family=family, feature_set=fs["set"], window=fs["window"])
            )
    return specs
