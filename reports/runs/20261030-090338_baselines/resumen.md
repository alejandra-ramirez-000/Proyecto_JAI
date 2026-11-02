# Corrida `baselines`

Métricas fuera de muestra (Leave-One-Year-Out). Conjunto `completo`: 45 filas, 9 folds. Conjunto `con_rezago`: 40 filas (2018–2025), 8 folds. IC 95 %: bootstrap por bloques de ejercicio.

## Regresión: intensidad ganadera (UG/ha)

| conjunto | modelo | n | MAE | MAE_ic95_inf | MAE_ic95_sup | RMSE | R2 | skill_vs_R1_promedio_departamental | skill_vs_R2_persistencia |
|---|---|---|---|---|---|---|---|---|---|
| completo | R1_promedio_departamental | 45 | 0.0263 | 0.0197 | 0.0341 | 0.0336 | 0.9694 | 0.0000 |  |
| con_rezago | R1_promedio_departamental | 40 | 0.0219 | 0.0171 | 0.0257 | 0.0302 | 0.9767 | 0.0000 | -0.1241 |
| con_rezago | R2_persistencia | 40 | 0.0195 | 0.0138 | 0.0253 | 0.0257 | 0.9830 | 0.1104 | 0.0000 |

## Clasificación: mortalidad ovina elevada

| conjunto | modelo | n | prevalencia | balanced_accuracy | balanced_accuracy_ic95_inf | balanced_accuracy_ic95_sup | roc_auc | average_precision | recall | especificidad | brier | tn | fp | fn | tp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | C1_clase_mayoritaria | 45 | 0.333 | 0.500 | 0.500 | 0.500 | 0.500 | 0.333 | 0.000 | 1.000 | 0.229 | 30 | 0 | 15 | 0 |
| con_rezago | C1_clase_mayoritaria | 40 | 0.275 | 0.500 | 0.500 | 0.500 | 0.500 | 0.275 | 0.000 | 1.000 | 0.199 | 29 | 0 | 11 | 0 |
| con_rezago | C2_persistencia_riesgo | 40 | 0.275 | 0.732 | 0.496 | 0.941 | 0.732 | 0.471 | 0.636 | 0.828 | 0.225 | 24 | 5 | 4 | 7 |
| completo | C3_historial_departamental | 45 | 0.333 | 0.500 | 0.500 | 0.500 | 0.500 | 0.333 | 0.000 | 1.000 | 0.229 | 30 | 0 | 15 | 0 |
| con_rezago | C3_historial_departamental | 40 | 0.275 | 0.500 | 0.500 | 0.500 | 0.500 | 0.275 | 0.000 | 1.000 | 0.199 | 29 | 0 | 11 | 0 |

Detalle por departamento y por ejercicio en los CSV `*_por_departamento.csv` y `*_por_anio.csv`.
