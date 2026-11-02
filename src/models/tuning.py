"""Pipelines y selección de hiperparámetros dentro de cada fold externo (secciones 16 y 18.2).

`TunedModel` es la función `fit_predict(train, test)` que usa la validación
externa. En cada llamada:

1. elige hiperparámetros con validación interna por año usando solo `train`
   (en clasificación, la etiqueta se recalcula también dentro de cada fold interno);
2. reajusta el pipeline completo (escalado + one-hot + modelo) sobre `train`;
3. predice `test` y registra hiperparámetros elegidos y coeficientes del fold.

Criterio de selección sobre las predicciones internas concatenadas:
- regresión: menor MAE;
- clasificación: menor log-loss balanceada, desempatando por balanced accuracy.
  (Versión 1.1. La versión 1.0 usaba balanced accuracy, que empataba en 0,5 en
  muchos folds y, con el desempate por regularización, elegía modelos casi
  constantes. Ver historial de la especificación.)

Las grillas se recorren de más a menos regularizado: ante empate exacto gana
la opción más regularizada.
"""

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import ParameterGrid
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.models.validation import (
    DEPT,
    LABEL,
    YEAR,
    add_high_mortality_label,
    balanced_accuracy_stat,
    balanced_log_loss_stat,
    inner_year_splits,
    mae_stat,
)


def build_pipeline(estimator, numeric: list[str], drop_first: bool = False) -> Pipeline:
    """Escalado de variables numéricas y one-hot del departamento, ajustados dentro del pipeline."""
    prep = ColumnTransformer(
        [
            ("num", StandardScaler(), numeric),
            ("dep", OneHotEncoder(drop="first" if drop_first else None, handle_unknown="ignore",
                                  sparse_output=False), [DEPT]),
        ]
    )
    return Pipeline([("prep", prep), ("model", clone(estimator))])


def _coefficients(pipeline: Pipeline) -> dict[str, float]:
    names = pipeline.named_steps["prep"].get_feature_names_out()
    model = pipeline.named_steps["model"]
    if hasattr(model, "coef_"):
        values = np.ravel(model.coef_)
    elif hasattr(model, "feature_importances_"):
        values = model.feature_importances_
    else:
        return {}
    return dict(zip(names, map(float, values)))


@dataclass
class TunedModel:
    estimator: object
    grid: dict
    numeric: list[str]
    task: str  # "regression" | "classification"
    target: str = "intensidad_ug_ha"
    quantile: float = 0.75
    drop_first: bool = False
    records: list = field(default_factory=list)

    def reset(self) -> None:
        self.records = []

    def _fit(self, train: pd.DataFrame, params: dict) -> Pipeline:
        pipeline = build_pipeline(self.estimator, self.numeric, self.drop_first)
        pipeline.set_params(**{f"model__{k}": v for k, v in params.items()})
        y = train[LABEL] if self.task == "classification" else train[self.target]
        return pipeline.fit(train, y)

    def _inner_score(self, train: pd.DataFrame, params: dict) -> tuple[float, float]:
        """Puntaje sobre las predicciones internas concatenadas (como en la validación externa)."""
        parts = []
        for inner_idx, val_idx in inner_year_splits(train):
            inner, val = train.iloc[inner_idx], train.iloc[val_idx]
            if self.task == "classification":
                inner, val, _ = add_high_mortality_label(inner, val, self.quantile)
                pipeline = self._fit(inner, params)
                proba = pipeline.predict_proba(val)[:, 1]
                parts.append({"y_true": val[LABEL].to_numpy(), "y_proba": proba, "y_pred": (proba >= 0.5).astype(int)})
            else:
                pipeline = self._fit(inner, params)
                parts.append({"y_true": val[self.target].to_numpy(), "y_pred": pipeline.predict(val)})
        pooled = {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}
        if self.task == "classification":
            return -balanced_log_loss_stat(pooled), balanced_accuracy_stat(pooled)
        return -mae_stat(pooled), 0.0

    def select(self, train: pd.DataFrame) -> tuple[dict, float]:
        candidates = list(ParameterGrid(self.grid))
        if len(candidates) == 1:
            return candidates[0], np.nan
        best, best_score = None, (-np.inf, -np.inf)
        for params in candidates:
            score = tuple(-np.inf if np.isnan(s) else s for s in self._inner_score(train, params))
            if score > best_score:
                best, best_score = params, score
        return best, best_score[0]

    def __call__(self, train: pd.DataFrame, test: pd.DataFrame):
        params, inner_score = self.select(train)
        pipeline = self._fit(train, params)
        self.records.append(
            {
                "fold": int(test[YEAR].iloc[0]),
                "hiperparametros": params,
                "puntaje_interno": inner_score,
                "coeficientes": _coefficients(pipeline),
            }
        )
        if self.task == "classification":
            proba = pipeline.predict_proba(test)[:, 1]
            return proba, (proba >= 0.5).astype(int)
        return pipeline.predict(test)
