# Corrida `exploratoria_hiperparametros_fijos`

> **Nota:** Ronda EXPLORATORIA definida después de ver la corrida 20261030-092748_modelos. Hiperparámetros fijos (Ridge alpha=1; logística C=1, class_weight='balanced'). No reemplaza a la corrida registrada ni constituye una evaluación no sesgada.

Métricas fuera de muestra (Leave-One-Year-Out). Conjunto `completo`: 45 filas, 9 folds. Conjunto `con_rezago`: 40 filas (2018–2025), 8 folds. IC 95 %: bootstrap por bloques de ejercicio.

Se muestran baselines, modelos principales y controles. Secundarios y sensibilidad (julio–octubre, bosque) están en los CSV de métricas.

## Criterios de la sección 20

### Regresión

| conjunto | modelo | rol | MAE | mejor_baseline | MAE_mejor_baseline | skill_vs_mejor_baseline | c1_supera_baselines | mejora_suficiente | skill_minimo_sin_un_anio | c3_robusto_a_quitar_un_anio | c4_estabilidad_signos | c5_deptos_que_mejoran | c6_sensibilidad_que_supera | c6_sensibilidades_evaluadas | skill_vs_control_sin_clima | c4_signos_estables | valor_predictivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | ridge_A_ejercicio_fijo | principal | 0.031 | R1_promedio_departamental | 0.026 | -0.191 | False | False | -0.400 | False | 1.000 | 1 | 0 | 1 |  | True | no |
| con_rezago | ridge_A_ejercicio_fijo | principal | 0.034 | R2_persistencia | 0.019 | -0.736 | False | False | -1.009 | False | 1.000 | 0 | 0 | 1 | -0.721 | True | no |
| con_rezago | ridge_C-A_ejercicio_fijo | principal | 0.021 | R2_persistencia | 0.019 | -0.084 | False | False | -0.168 | False | 0.750 | 2 | 0 | 1 | -0.074 | False | no |
| completo | ridge_B_ejercicio_fijo | principal | 0.033 | R1_promedio_departamental | 0.026 | -0.258 | False | False | -0.496 | False | 0.556 | 0 | 0 | 1 |  | False | no |
| con_rezago | ridge_B_ejercicio_fijo | principal | 0.034 | R2_persistencia | 0.019 | -0.727 | False | False | -1.028 | False | 0.500 | 0 | 0 | 1 | -0.711 | False | no |
| con_rezago | ridge_C-B_ejercicio_fijo | principal | 0.022 | R2_persistencia | 0.019 | -0.141 | False | False | -0.197 | False | 0.750 | 1 | 0 | 1 | -0.131 | False | no |
| con_rezago | ridge_H_sin_clima_fijo | control | 0.020 | R2_persistencia | 0.019 | -0.009 | False | False | -0.055 | False |  | 3 | 0 | 0 | 0.000 | False | no aplica (control) |

### Clasificación

| conjunto | modelo | rol | balanced_accuracy | roc_auc | mejor_baseline | balanced_accuracy_mejor_baseline | diferencia_vs_mejor_baseline | c1_supera_baselines | mejora_suficiente | diferencia_minima_sin_un_anio | c3_robusto_a_quitar_un_anio | c4_estabilidad_signos | c5_deptos_que_mejoran | c6_sensibilidad_que_supera | c6_sensibilidades_evaluadas | diferencia_vs_control_sin_clima | c4_signos_estables | valor_predictivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | logistica_A_ejercicio_fijo | principal | 0.550 | 0.536 | C1_clase_mayoritaria | 0.500 | 0.050 | True | True | 0.003 | True | 0.556 | 1 | 0 | 1 |  | False | no |
| con_rezago | logistica_A_ejercicio_fijo | principal | 0.514 | 0.483 | C2_persistencia_riesgo | 0.732 | -0.218 | False | False | -0.301 | False | 0.625 | 0 | 0 | 1 | -0.188 | False | no |
| con_rezago | logistica_C-A_ejercicio_fijo | principal | 0.538 | 0.527 | C2_persistencia_riesgo | 0.732 | -0.194 | False | False | -0.280 | False | 0.875 | 0 | 0 | 1 | -0.165 | True | no |
| completo | logistica_B_ejercicio_fijo | principal | 0.417 | 0.367 | C1_clase_mayoritaria | 0.500 | -0.083 | False | False | -0.113 | False | 0.778 | 0 | 0 | 1 |  | False | no |
| con_rezago | logistica_B_ejercicio_fijo | principal | 0.320 | 0.282 | C2_persistencia_riesgo | 0.732 | -0.412 | False | False | -0.528 | False | 0.750 | 0 | 0 | 1 | -0.382 | False | no |
| con_rezago | logistica_C-B_ejercicio_fijo | principal | 0.332 | 0.282 | C2_persistencia_riesgo | 0.732 | -0.400 | False | False | -0.516 | False | 0.625 | 0 | 0 | 1 | -0.370 | False | no |
| con_rezago | logistica_H_sin_clima_fijo | control | 0.702 | 0.596 | C2_persistencia_riesgo | 0.732 | -0.030 | False | False | -0.130 | False |  | 0 | 0 | 0 | 0.000 | False | no aplica (control) |

## Regresión: intensidad ganadera (UG/ha)

| conjunto | modelo | rol | n | MAE | MAE_ic95_inf | MAE_ic95_sup | RMSE | R2 | skill_vs_R1_promedio_departamental | skill_vs_R2_persistencia |
|---|---|---|---|---|---|---|---|---|---|---|
| completo | R1_promedio_departamental | baseline | 45 | 0.0263 | 0.0197 | 0.0341 | 0.0336 | 0.9694 | 0.0000 |  |
| con_rezago | R1_promedio_departamental | baseline | 40 | 0.0219 | 0.0171 | 0.0257 | 0.0302 | 0.9767 | 0.0000 | -0.1241 |
| con_rezago | R2_persistencia | baseline | 40 | 0.0195 | 0.0138 | 0.0253 | 0.0257 | 0.9830 | 0.1104 | 0.0000 |
| completo | ridge_A_ejercicio_fijo | principal | 45 | 0.0313 | 0.0232 | 0.0393 | 0.0431 | 0.9498 | -0.1914 |  |
| con_rezago | ridge_A_ejercicio_fijo | principal | 40 | 0.0338 | 0.0247 | 0.0429 | 0.0456 | 0.9466 | -0.5447 | -0.7363 |
| con_rezago | ridge_C-A_ejercicio_fijo | principal | 40 | 0.0211 | 0.0152 | 0.0270 | 0.0280 | 0.9799 | 0.0358 | -0.0838 |
| completo | ridge_B_ejercicio_fijo | principal | 45 | 0.0330 | 0.0229 | 0.0429 | 0.0440 | 0.9477 | -0.2584 |  |
| con_rezago | ridge_B_ejercicio_fijo | principal | 40 | 0.0337 | 0.0230 | 0.0446 | 0.0453 | 0.9473 | -0.5361 | -0.7267 |
| con_rezago | ridge_C-B_ejercicio_fijo | principal | 40 | 0.0223 | 0.0158 | 0.0288 | 0.0290 | 0.9784 | -0.0154 | -0.1414 |
| con_rezago | ridge_H_sin_clima_fijo | control | 40 | 0.0197 | 0.0147 | 0.0245 | 0.0253 | 0.9836 | 0.1025 | -0.0089 |

## Clasificación: mortalidad ovina elevada

| conjunto | modelo | rol | n | prevalencia | balanced_accuracy | balanced_accuracy_ic95_inf | balanced_accuracy_ic95_sup | roc_auc | roc_auc_promedio_folds | average_precision | recall | especificidad | brier | tn | fp | fn | tp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | C1_clase_mayoritaria | baseline | 45 | 0.333 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.333 | 0.000 | 1.000 | 0.229 | 30 | 0 | 15 | 0 |
| con_rezago | C1_clase_mayoritaria | baseline | 40 | 0.275 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.275 | 0.000 | 1.000 | 0.199 | 29 | 0 | 11 | 0 |
| con_rezago | C2_persistencia_riesgo | baseline | 40 | 0.275 | 0.732 | 0.496 | 0.941 | 0.732 | 0.646 | 0.471 | 0.636 | 0.828 | 0.225 | 24 | 5 | 4 | 7 |
| completo | C3_historial_departamental | baseline | 45 | 0.333 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.333 | 0.000 | 1.000 | 0.229 | 30 | 0 | 15 | 0 |
| con_rezago | C3_historial_departamental | baseline | 40 | 0.275 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.275 | 0.000 | 1.000 | 0.199 | 29 | 0 | 11 | 0 |
| completo | logistica_A_ejercicio_fijo | principal | 45 | 0.333 | 0.550 | 0.412 | 0.707 | 0.536 | 0.567 | 0.411 | 0.533 | 0.567 | 0.265 | 17 | 13 | 7 | 8 |
| con_rezago | logistica_A_ejercicio_fijo | principal | 40 | 0.275 | 0.514 | 0.400 | 0.695 | 0.483 | 0.458 | 0.331 | 0.545 | 0.483 | 0.284 | 14 | 15 | 5 | 6 |
| con_rezago | logistica_C-A_ejercicio_fijo | principal | 40 | 0.275 | 0.538 | 0.401 | 0.682 | 0.527 | 0.500 | 0.314 | 0.455 | 0.621 | 0.265 | 18 | 11 | 6 | 5 |
| completo | logistica_B_ejercicio_fijo | principal | 45 | 0.333 | 0.417 | 0.336 | 0.538 | 0.367 | 0.417 | 0.272 | 0.467 | 0.367 | 0.291 | 11 | 19 | 8 | 7 |
| con_rezago | logistica_B_ejercicio_fijo | principal | 40 | 0.275 | 0.320 | 0.208 | 0.534 | 0.282 | 0.375 | 0.209 | 0.364 | 0.276 | 0.327 | 8 | 21 | 7 | 4 |
| con_rezago | logistica_C-B_ejercicio_fijo | principal | 40 | 0.275 | 0.332 | 0.214 | 0.470 | 0.282 | 0.333 | 0.211 | 0.182 | 0.483 | 0.314 | 14 | 15 | 9 | 2 |
| con_rezago | logistica_H_sin_clima_fijo | control | 40 | 0.275 | 0.702 | 0.422 | 0.889 | 0.596 | 0.708 | 0.343 | 0.818 | 0.586 | 0.249 | 17 | 12 | 2 | 9 |

Detalle por departamento y por ejercicio en los CSV `*_por_departamento.csv` y `*_por_anio.csv`; hiperparámetros y coeficientes por fold en `*_hiperparametros.csv` y `*_coeficientes.csv`.
