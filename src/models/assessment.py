"""Criterios para afirmar valor predictivo (sección 20) y tabla única de resultados.

Para cada modelo principal y control, en cada conjunto de evaluación:

1. supera a todos los baselines del conjunto en la métrica primaria;
2. fuera de muestra (todas las métricas lo son por construcción);
3. la mejora frente al mejor baseline se mantiene al quitar cualquier ejercicio;
4. los coeficientes climáticos mantienen el signo en al menos 80 % de los folds;
5. mejora al mejor baseline en al menos 3 de los 5 departamentos;
6. alguna especificación de sensibilidad (julio–octubre o modelo secundario
   con las mismas variables) también supera al mejor baseline;
7. sin fuga temporal (garantizado por la validación y sus tests).

Además se informa la mejora frente al control H (rezago + departamento, sin
clima), que responde la pregunta principal: ¿aporta el clima por encima de la
historia propia?
"""

import numpy as np
import pandas as pd

from src.models.validation import YEAR, balanced_accuracy_stat, mae_skill

SIGN_STABILITY_MIN = 0.8
MIN_DEPARTMENTS = 3


def _arrays(df: pd.DataFrame) -> dict:
    return {c: df[c].to_numpy() for c in ["y_true", "y_pred"]}


def _mae(df: pd.DataFrame) -> float:
    return float(np.mean(np.abs(df["y_true"] - df["y_pred"])))


def _balanced_accuracy(df: pd.DataFrame) -> float:
    return balanced_accuracy_stat(_arrays(df))


def sign_stability(coefs: pd.DataFrame | None, model: str, set_name: str, lag_columns: set[str]) -> float:
    """Mínimo, entre variables climáticas, de la fracción de folds con el signo mayoritario.

    NaN si el modelo no tiene coeficientes lineales climáticos (árboles o control sin clima).
    """
    if coefs is None or coefs.empty:
        return np.nan
    data = coefs[(coefs["modelo"] == model) & (coefs["conjunto"] == set_name)]
    data = data[data["variable"].str.startswith("num__")]
    data = data[~data["variable"].str.removeprefix("num__").isin(lag_columns)]
    if data.empty:
        return np.nan
    fractions = []
    for _, values in data.groupby("variable")["valor"]:
        signs = np.sign(values.to_numpy())
        majority = 1 if (signs > 0).sum() >= (signs < 0).sum() else -1
        fractions.append(float(np.mean(signs == majority)))
    return min(fractions)


def _counterparts(summary: pd.DataFrame, row: pd.Series) -> pd.DataFrame:
    """Especificaciones de sensibilidad del mismo conjunto de variables y conjunto de evaluación."""
    same = summary[(summary["conjunto"] == row["conjunto"]) & (summary["modelo"] != row["modelo"])]
    july_october = same[(same["familia"] == row["familia"]) & (same["conjunto_variables"] == row["conjunto_variables"])
                        & (same["ventana"] != row["ventana"])]
    secondary = same[(same["rol"].isin(["secundario", "sensibilidad"])) & (same["familia"] != row["familia"])
                     & (same["conjunto_variables"] == row["conjunto_variables"]) & (same["ventana"] == row["ventana"])]
    return pd.concat([july_october, secondary])


def _control(summary: pd.DataFrame, set_name: str) -> pd.Series | None:
    control = summary[(summary["conjunto"] == set_name) & (summary["rol"] == "control")]
    return control.iloc[0] if len(control) else None


def _verdict(row: dict) -> str:
    if row["rol"] != "principal":
        return "no aplica (control)"
    checks = [row["c1_supera_baselines"], row["c3_robusto_a_quitar_un_anio"], row["c4_signos_estables"],
              row["c5_deptos_que_mejoran"] >= MIN_DEPARTMENTS, row["c6_sensibilidad_que_supera"] > 0,
              row["mejora_suficiente"]]
    return "sí" if all(checks) else "no"


def regression_criteria(tables: dict[str, pd.DataFrame], cfg: dict, lag_columns: set[str]) -> pd.DataFrame:
    summary, oof = tables["regresion_metricas"], tables["regresion_predicciones"]
    coefs = tables.get("regresion_coeficientes")
    rows = []
    for _, m in summary[summary["rol"].isin(["principal", "control"])].iterrows():
        baselines = summary[(summary["conjunto"] == m["conjunto"]) & (summary["rol"] == "baseline")]
        best = baselines.loc[baselines["MAE"].idxmin()]
        model_oof = oof[(oof["conjunto"] == m["conjunto"]) & (oof["modelo"] == m["modelo"])]
        best_oof = oof[(oof["conjunto"] == m["conjunto"]) & (oof["modelo"] == best["modelo"])]
        skill_without_year = [
            mae_skill(_mae(model_oof[model_oof[YEAR] != y]), _mae(best_oof[best_oof[YEAR] != y]))
            for y in sorted(model_oof[YEAR].unique())
        ]
        dept_model = model_oof.groupby("Departamento").apply(_mae, include_groups=False)
        dept_best = best_oof.groupby("Departamento").apply(_mae, include_groups=False)
        sensitivity = _counterparts(summary, m)
        control = _control(summary, m["conjunto"])
        skill = mae_skill(m["MAE"], best["MAE"])
        row = {
            "conjunto": m["conjunto"], "modelo": m["modelo"], "rol": m["rol"], "MAE": m["MAE"],
            "mejor_baseline": best["modelo"], "MAE_mejor_baseline": best["MAE"],
            "skill_vs_mejor_baseline": skill,
            "c1_supera_baselines": bool((m["MAE"] < baselines["MAE"]).all()),
            "mejora_suficiente": bool(skill >= cfg["validation"]["weak_improvement_mae"]),
            "skill_minimo_sin_un_anio": min(skill_without_year),
            "c3_robusto_a_quitar_un_anio": bool(min(skill_without_year) > 0),
            "c4_estabilidad_signos": sign_stability(coefs, m["modelo"], m["conjunto"], lag_columns),
            "c5_deptos_que_mejoran": int((dept_model < dept_best.reindex(dept_model.index)).sum()),
            "c6_sensibilidad_que_supera": int((sensitivity["MAE"] < best["MAE"]).sum()),
            "c6_sensibilidades_evaluadas": len(sensitivity),
            "skill_vs_control_sin_clima": mae_skill(m["MAE"], control["MAE"]) if control is not None else np.nan,
        }
        row["c4_signos_estables"] = bool(row["c4_estabilidad_signos"] >= SIGN_STABILITY_MIN)
        row["valor_predictivo"] = _verdict(row)
        rows.append(row)
    return pd.DataFrame(rows)


def classification_criteria(tables: dict[str, pd.DataFrame], cfg: dict, lag_columns: set[str]) -> pd.DataFrame:
    summary, oof = tables["clasificacion_metricas"], tables["clasificacion_predicciones"]
    coefs = tables.get("clasificacion_coeficientes")
    rows = []
    for _, m in summary[summary["rol"].isin(["principal", "control"])].iterrows():
        baselines = summary[(summary["conjunto"] == m["conjunto"]) & (summary["rol"] == "baseline")]
        best = baselines.sort_values(["balanced_accuracy", "roc_auc"], ascending=False).iloc[0]
        model_oof = oof[(oof["conjunto"] == m["conjunto"]) & (oof["modelo"] == m["modelo"])]
        best_oof = oof[(oof["conjunto"] == m["conjunto"]) & (oof["modelo"] == best["modelo"])]
        diff_without_year = [
            _balanced_accuracy(model_oof[model_oof[YEAR] != y]) - _balanced_accuracy(best_oof[best_oof[YEAR] != y])
            for y in sorted(model_oof[YEAR].unique())
        ]
        # Por departamento hay pocos positivos: se comparan aciertos, no balanced accuracy.
        correct_model = (model_oof["y_true"] == model_oof["y_pred"]).groupby(model_oof["Departamento"]).sum()
        correct_best = (best_oof["y_true"] == best_oof["y_pred"]).groupby(best_oof["Departamento"]).sum()
        sensitivity = _counterparts(summary, m)
        control = _control(summary, m["conjunto"])
        diff = m["balanced_accuracy"] - best["balanced_accuracy"]
        row = {
            "conjunto": m["conjunto"], "modelo": m["modelo"], "rol": m["rol"],
            "balanced_accuracy": m["balanced_accuracy"], "roc_auc": m["roc_auc"],
            "mejor_baseline": best["modelo"], "balanced_accuracy_mejor_baseline": best["balanced_accuracy"],
            "diferencia_vs_mejor_baseline": diff,
            "c1_supera_baselines": bool((m["balanced_accuracy"] > baselines["balanced_accuracy"]).all()),
            "mejora_suficiente": bool(diff > 0),
            "diferencia_minima_sin_un_anio": float(np.nanmin(diff_without_year)),
            "c3_robusto_a_quitar_un_anio": bool(np.nanmin(diff_without_year) > 0),
            "c4_estabilidad_signos": sign_stability(coefs, m["modelo"], m["conjunto"], lag_columns),
            "c5_deptos_que_mejoran": int((correct_model > correct_best.reindex(correct_model.index)).sum()),
            "c6_sensibilidad_que_supera": int((sensitivity["balanced_accuracy"] > best["balanced_accuracy"]).sum()),
            "c6_sensibilidades_evaluadas": len(sensitivity),
            "diferencia_vs_control_sin_clima": (m["balanced_accuracy"] - control["balanced_accuracy"]
                                                if control is not None else np.nan),
        }
        row["c4_signos_estables"] = bool(row["c4_estabilidad_signos"] >= SIGN_STABILITY_MIN)
        row["valor_predictivo"] = _verdict(row)
        rows.append(row)
    return pd.DataFrame(rows)
