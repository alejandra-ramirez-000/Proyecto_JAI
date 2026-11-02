"""Validación Leave-One-Year-Out, etiqueta de mortalidad elevada por fold, métricas y bootstrap por año.

Reglas contra fuga (sección 16) que este módulo garantiza:
- cada fold deja afuera un ejercicio completo con sus cinco departamentos;
- el umbral P75 de mortalidad elevada se calcula solo con el entrenamiento del fold;
- las funciones de predicción reciben el entrenamiento y la prueba por separado,
  así que cualquier ajuste (escalado, codificación, hiperparámetros) ocurre dentro del fold;
- las métricas se calculan sobre las predicciones fuera de muestra concatenadas.
"""

from collections.abc import Callable, Iterator
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.stats import rankdata
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import LeaveOneGroupOut

from src.data.build_panel import LAG_COLUMNS

YEAR = "AnioEjercicio"
DEPT = "DepartamentoCodigo"
ID_COLUMNS = [DEPT, "Departamento", YEAR]
LABEL = "mortalidad_elevada"
LAG_LABEL = "mortalidad_lag1_elevada"
THRESHOLD = "umbral_mortalidad_elevada"

# Conjuntos de evaluación: todo el panel (sin rezagos) o solo filas con rezago (sección 18.1).
EVALUATION_SETS = {"completo": False, "con_rezago": True}


@dataclass(frozen=True)
class Fold:
    year: int
    train: pd.DataFrame
    test: pd.DataFrame


def evaluation_set(panel: pd.DataFrame, with_lag: bool) -> pd.DataFrame:
    """Panel completo (45 filas) o restringido a filas con rezagos (40 filas, 2018–2025).

    Todos los modelos comparados en un conjunto usan exactamente las mismas filas.
    """
    data = panel.dropna(subset=list(LAG_COLUMNS.values())) if with_lag else panel
    return data.sort_values([YEAR, DEPT]).reset_index(drop=True)


def loyo_folds(data: pd.DataFrame) -> Iterator[Fold]:
    """Un fold por ejercicio: prueba = los cinco departamentos de ese ejercicio."""
    for year in sorted(data[YEAR].unique()):
        is_test = data[YEAR] == year
        yield Fold(year=int(year), train=data[~is_test].copy(), test=data[is_test].copy())


def inner_year_splits(train: pd.DataFrame) -> list[tuple[np.ndarray, np.ndarray]]:
    """Validación interna por año dentro del entrenamiento externo (sección 18.2).

    Devuelve índices posicionales para usar como `cv` de scikit-learn.
    """
    return list(LeaveOneGroupOut().split(train, groups=train[YEAR]))


def add_high_mortality_label(train: pd.DataFrame, test: pd.DataFrame, quantile: float):
    """Etiqueta de mortalidad elevada con umbral departamental calculado solo en entrenamiento.

    `mortalidad_elevada` = 1 si la tasa supera el percentil del departamento en
    entrenamiento. También etiqueta el rezago con el mismo umbral, para el
    baseline de persistencia de riesgo (C2).
    """
    thresholds = train.groupby(DEPT)["tasa_mortalidad_1000"].quantile(quantile)
    labelled = []
    for df in (train, test):
        df = df.copy()
        df[THRESHOLD] = df[DEPT].map(thresholds)
        if df[THRESHOLD].isna().any():
            raise ValueError("Departamento de prueba sin historia en entrenamiento")
        df[LABEL] = (df["tasa_mortalidad_1000"] > df[THRESHOLD]).astype(int)
        lag_above = df["mortalidad_lag1"] > df[THRESHOLD]
        df[LAG_LABEL] = lag_above.astype(float).where(df["mortalidad_lag1"].notna())
        labelled.append(df)
    return labelled[0], labelled[1], thresholds


# ---------------------------------------------------------------------------
# Validación cruzada
# ---------------------------------------------------------------------------

RegressionFn = Callable[[pd.DataFrame, pd.DataFrame], np.ndarray]
ClassificationFn = Callable[[pd.DataFrame, pd.DataFrame], tuple[np.ndarray, np.ndarray]]


def cross_validate_regression(data: pd.DataFrame, fit_predict: RegressionFn, target: str, model: str) -> pd.DataFrame:
    """Predicciones fuera de muestra concatenadas de todos los folds."""
    parts = []
    for fold in loyo_folds(data):
        predictions = np.asarray(fit_predict(fold.train, fold.test), dtype=float)
        parts.append(fold.test[ID_COLUMNS].assign(fold=fold.year, y_true=fold.test[target].values, y_pred=predictions))
    return pd.concat(parts, ignore_index=True).assign(modelo=model)


def cross_validate_classification(
    data: pd.DataFrame, fit_predict: ClassificationFn, model: str, quantile: float
) -> pd.DataFrame:
    """Predicciones fuera de muestra; la etiqueta se recalcula en cada fold."""
    parts = []
    for fold in loyo_folds(data):
        train, test, _ = add_high_mortality_label(fold.train, fold.test, quantile)
        proba, predicted = fit_predict(train, test)
        parts.append(
            test[ID_COLUMNS + [THRESHOLD]].assign(
                fold=fold.year,
                y_true=test[LABEL].values,
                y_proba=np.asarray(proba, dtype=float),
                y_pred=np.asarray(predicted, dtype=int),
                prevalencia_entrenamiento=train[LABEL].mean(),
            )
        )
    return pd.concat(parts, ignore_index=True).assign(modelo=model)


# ---------------------------------------------------------------------------
# Métricas (sección 19)
# ---------------------------------------------------------------------------


def regression_metrics(oof: pd.DataFrame) -> dict:
    y, p = oof["y_true"], oof["y_pred"]
    return {
        "n": len(oof),
        "MAE": mean_absolute_error(y, p),
        "RMSE": float(np.sqrt(mean_squared_error(y, p))),
        "R2": r2_score(y, p) if len(oof) > 1 else np.nan,
    }


def classification_metrics(oof: pd.DataFrame) -> dict:
    y, proba, pred = oof["y_true"], oof["y_proba"], oof["y_pred"]
    both_classes = y.nunique() == 2
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {
        "n": len(oof),
        "prevalencia": y.mean(),
        "balanced_accuracy": balanced_accuracy_score(y, pred) if both_classes else np.nan,
        "roc_auc": roc_auc_score(y, proba) if both_classes else np.nan,
        "average_precision": average_precision_score(y, proba) if both_classes else np.nan,
        "f1": f1_score(y, pred, zero_division=0),
        "recall": recall_score(y, pred, zero_division=0),
        "precision": precision_score(y, pred, zero_division=0),
        "especificidad": tn / (tn + fp) if tn + fp else np.nan,
        "brier": brier_score_loss(y, proba),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def mean_fold_auc(oof: pd.DataFrame) -> dict:
    """AUC promedio de los folds que tienen ambas clases (diagnóstico, no métrica primaria).

    La sección 18.3 fija el AUC concatenado como métrica principal. Este
    promedio no mezcla probabilidades de modelos distintos y ayuda a detectar
    cuándo el AUC concatenado está distorsionado por diferencias de escala
    entre folds.
    """
    values = [roc_auc_score(g["y_true"], g["y_proba"]) for _, g in oof.groupby("fold") if g["y_true"].nunique() == 2]
    return {"roc_auc_promedio_folds": float(np.mean(values)) if values else np.nan, "folds_con_ambas_clases": len(values)}


def metrics_by(oof: pd.DataFrame, metric_fn: Callable[[pd.DataFrame], dict], by: str) -> pd.DataFrame:
    rows = [{by: key, **metric_fn(group)} for key, group in oof.groupby(by)]
    return pd.DataFrame(rows)


def mae_skill(model_mae: float, baseline_mae: float) -> float:
    """Skill = 1 − MAE_modelo / MAE_baseline (sección 19.1)."""
    return 1 - model_mae / baseline_mae


# Estadísticos livianos en numpy para el bootstrap (miles de remuestras).
# Reciben un diccionario columna -> array; los tests verifican que coinciden con scikit-learn.


def mae_stat(d: dict) -> float:
    return float(np.mean(np.abs(d["y_true"] - d["y_pred"])))


def balanced_accuracy_stat(d: dict) -> float:
    y, pred = d["y_true"], d["y_pred"]
    pos = y == 1
    if pos.all() or not pos.any():
        return np.nan
    return float((np.mean(pred[pos] == 1) + np.mean(pred[~pos] == 0)) / 2)


def balanced_log_loss_stat(d: dict, eps: float = 1e-15) -> float:
    """Pérdida logarítmica con las dos clases pesadas por igual (menor es mejor).

    Equivale a promediar la log-loss de cada clase. A diferencia de la balanced
    accuracy, es continua y penaliza un modelo casi constante: predecir siempre
    la prevalencia da una pérdida mayor que ln 2, la de predecir 0,5.
    """
    y = d["y_true"]
    p = np.clip(d["y_proba"], eps, 1 - eps)
    pos = y == 1
    if pos.all() or not pos.any():
        return np.nan
    return float((-np.mean(np.log(p[pos])) - np.mean(np.log(1 - p[~pos]))) / 2)


def roc_auc_stat(d: dict) -> float:
    """AUC por Mann–Whitney con rangos promedio para empates."""
    y, score = d["y_true"], d["y_proba"]
    pos = y == 1
    n_pos, n_neg = int(pos.sum()), int((~pos).sum())
    if not n_pos or not n_neg:
        return np.nan
    ranks = rankdata(score)
    return float((ranks[pos].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def year_block_bootstrap(
    oof: pd.DataFrame, statistic: Callable[[dict], float], columns: list[str], n_boot: int, seed: int
) -> dict:
    """Intervalo percentil 95 % remuestreando ejercicios completos, nunca filas sueltas (sección 18.4)."""
    rng = np.random.default_rng(seed)
    blocks = [{c: group[c].to_numpy() for c in columns} for _, group in oof.groupby(YEAR)]
    values = []
    for _ in range(n_boot):
        chosen = rng.integers(0, len(blocks), size=len(blocks))
        sample = {c: np.concatenate([blocks[i][c] for i in chosen]) for c in columns}
        values.append(statistic(sample))
    values = np.array(values, dtype=float)
    valid = values[~np.isnan(values)]
    return {
        "ic95_inf": float(np.percentile(valid, 2.5)) if len(valid) else np.nan,
        "ic95_sup": float(np.percentile(valid, 97.5)) if len(valid) else np.nan,
        "remuestras_validas": int(len(valid)),
    }
