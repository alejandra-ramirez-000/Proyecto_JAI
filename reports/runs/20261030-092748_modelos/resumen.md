# Corrida `modelos`

Métricas fuera de muestra (Leave-One-Year-Out). Conjunto `completo`: 45 filas, 9 folds. Conjunto `con_rezago`: 40 filas (2018–2025), 8 folds. IC 95 %: bootstrap por bloques de ejercicio.

Se muestran baselines, modelos principales y controles. Secundarios y sensibilidad (julio–octubre, bosque) están en los CSV de métricas.

## Criterios de la sección 20

### Regresión

| conjunto | modelo | rol | MAE | mejor_baseline | MAE_mejor_baseline | skill_vs_mejor_baseline | c1_supera_baselines | mejora_suficiente | skill_minimo_sin_un_anio | c3_robusto_a_quitar_un_anio | c4_estabilidad_signos | c5_deptos_que_mejoran | c6_sensibilidad_que_supera | c6_sensibilidades_evaluadas | skill_vs_control_sin_clima | c4_signos_estables | valor_predictivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | ridge_A_ejercicio | principal | 0.027 | R1_promedio_departamental | 0.026 | -0.023 | False | False | -0.089 | False | 1.000 | 2 | 0 | 4 |  | True | no |
| con_rezago | ridge_A_ejercicio | principal | 0.025 | R2_persistencia | 0.019 | -0.263 | False | False | -0.411 | False | 1.000 | 1 | 0 | 4 | -0.301 | True | no |
| con_rezago | ridge_C-A_ejercicio | principal | 0.021 | R2_persistencia | 0.019 | -0.079 | False | False | -0.142 | False | 0.875 | 3 | 1 | 4 | -0.112 | True | no |
| completo | ridge_B_ejercicio | principal | 0.029 | R1_promedio_departamental | 0.026 | -0.090 | False | False | -0.141 | False | 0.667 | 1 | 1 | 4 |  | False | no |
| con_rezago | ridge_B_ejercicio | principal | 0.024 | R2_persistencia | 0.019 | -0.225 | False | False | -0.395 | False | 0.750 | 2 | 0 | 4 | -0.262 | False | no |
| con_rezago | ridge_C-B_ejercicio | principal | 0.021 | R2_persistencia | 0.019 | -0.077 | False | False | -0.147 | False | 0.625 | 2 | 0 | 4 | -0.109 | False | no |
| con_rezago | ridge_H_sin_clima | control | 0.019 | R2_persistencia | 0.019 | 0.029 | True | False | -0.041 | False |  | 4 | 0 | 0 | 0.000 | False | no aplica (control) |

### Clasificación

| conjunto | modelo | rol | balanced_accuracy | roc_auc | mejor_baseline | balanced_accuracy_mejor_baseline | diferencia_vs_mejor_baseline | c1_supera_baselines | mejora_suficiente | diferencia_minima_sin_un_anio | c3_robusto_a_quitar_un_anio | c4_estabilidad_signos | c5_deptos_que_mejoran | c6_sensibilidad_que_supera | c6_sensibilidades_evaluadas | diferencia_vs_control_sin_clima | c4_signos_estables | valor_predictivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | logistica_A_ejercicio | principal | 0.417 | 0.362 | C1_clase_mayoritaria | 0.500 | -0.083 | False | False | -0.121 | False | 0.556 | 1 | 1 | 4 |  | False | no |
| con_rezago | logistica_A_ejercicio | principal | 0.487 | 0.498 | C2_persistencia_riesgo | 0.732 | -0.245 | False | False | -0.314 | False | 0.500 | 0 | 0 | 4 | 0.143 | False | no |
| con_rezago | logistica_C-A_ejercicio | principal | 0.408 | 0.298 | C2_persistencia_riesgo | 0.732 | -0.324 | False | False | -0.387 | False | 0.875 | 0 | 0 | 4 | 0.063 | True | no |
| completo | logistica_B_ejercicio | principal | 0.383 | 0.202 | C1_clase_mayoritaria | 0.500 | -0.117 | False | False | -0.140 | False | 0.667 | 0 | 2 | 4 |  | False | no |
| con_rezago | logistica_B_ejercicio | principal | 0.516 | 0.436 | C2_persistencia_riesgo | 0.732 | -0.216 | False | False | -0.314 | False | 0.625 | 0 | 0 | 4 | 0.171 | False | no |
| con_rezago | logistica_C-B_ejercicio | principal | 0.442 | 0.245 | C2_persistencia_riesgo | 0.732 | -0.290 | False | False | -0.353 | False | 0.625 | 0 | 0 | 4 | 0.097 | False | no |
| con_rezago | logistica_H_sin_clima | control | 0.345 | 0.348 | C2_persistencia_riesgo | 0.732 | -0.387 | False | False | -0.468 | False |  | 0 | 0 | 0 | 0.000 | False | no aplica (control) |

## Regresión: intensidad ganadera (UG/ha)

| conjunto | modelo | rol | n | MAE | MAE_ic95_inf | MAE_ic95_sup | RMSE | R2 | skill_vs_R1_promedio_departamental | skill_vs_R2_persistencia |
|---|---|---|---|---|---|---|---|---|---|---|
| completo | R1_promedio_departamental | baseline | 45 | 0.0263 | 0.0197 | 0.0341 | 0.0336 | 0.9694 | 0.0000 |  |
| con_rezago | R1_promedio_departamental | baseline | 40 | 0.0219 | 0.0171 | 0.0257 | 0.0302 | 0.9767 | 0.0000 | -0.1241 |
| con_rezago | R2_persistencia | baseline | 40 | 0.0195 | 0.0138 | 0.0253 | 0.0257 | 0.9830 | 0.1104 | 0.0000 |
| completo | ridge_A_ejercicio | principal | 45 | 0.0269 | 0.0211 | 0.0327 | 0.0350 | 0.9669 | -0.0229 |  |
| con_rezago | ridge_A_ejercicio | principal | 40 | 0.0246 | 0.0192 | 0.0302 | 0.0333 | 0.9716 | -0.1239 | -0.2633 |
| con_rezago | ridge_C-A_ejercicio | principal | 40 | 0.0210 | 0.0160 | 0.0260 | 0.0272 | 0.9810 | 0.0399 | -0.0793 |
| completo | ridge_B_ejercicio | principal | 45 | 0.0286 | 0.0229 | 0.0346 | 0.0361 | 0.9649 | -0.0903 |  |
| con_rezago | ridge_B_ejercicio | principal | 40 | 0.0239 | 0.0204 | 0.0268 | 0.0327 | 0.9726 | -0.0894 | -0.2245 |
| con_rezago | ridge_C-B_ejercicio | principal | 40 | 0.0210 | 0.0159 | 0.0267 | 0.0274 | 0.9807 | 0.0422 | -0.0766 |
| con_rezago | ridge_H_sin_clima | control | 40 | 0.0189 | 0.0150 | 0.0230 | 0.0243 | 0.9849 | 0.1365 | 0.0293 |

## Clasificación: mortalidad ovina elevada

| conjunto | modelo | rol | n | prevalencia | balanced_accuracy | balanced_accuracy_ic95_inf | balanced_accuracy_ic95_sup | roc_auc | average_precision | recall | especificidad | brier | tn | fp | fn | tp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | C1_clase_mayoritaria | baseline | 45 | 0.333 | 0.500 | 0.500 | 0.500 | 0.500 | 0.333 | 0.000 | 1.000 | 0.229 | 30 | 0 | 15 | 0 |
| con_rezago | C1_clase_mayoritaria | baseline | 40 | 0.275 | 0.500 | 0.500 | 0.500 | 0.500 | 0.275 | 0.000 | 1.000 | 0.199 | 29 | 0 | 11 | 0 |
| con_rezago | C2_persistencia_riesgo | baseline | 40 | 0.275 | 0.732 | 0.496 | 0.941 | 0.732 | 0.471 | 0.636 | 0.828 | 0.225 | 24 | 5 | 4 | 7 |
| completo | C3_historial_departamental | baseline | 45 | 0.333 | 0.500 | 0.500 | 0.500 | 0.500 | 0.333 | 0.000 | 1.000 | 0.229 | 30 | 0 | 15 | 0 |
| con_rezago | C3_historial_departamental | baseline | 40 | 0.275 | 0.500 | 0.500 | 0.500 | 0.500 | 0.275 | 0.000 | 1.000 | 0.199 | 29 | 0 | 11 | 0 |
| completo | logistica_A_ejercicio | principal | 45 | 0.333 | 0.417 | 0.309 | 0.523 | 0.362 | 0.271 | 0.067 | 0.767 | 0.273 | 23 | 7 | 14 | 1 |
| con_rezago | logistica_A_ejercicio | principal | 40 | 0.275 | 0.487 | 0.384 | 0.593 | 0.498 | 0.293 | 0.182 | 0.793 | 0.244 | 23 | 6 | 9 | 2 |
| con_rezago | logistica_C-A_ejercicio | principal | 40 | 0.275 | 0.408 | 0.328 | 0.531 | 0.298 | 0.220 | 0.091 | 0.724 | 0.272 | 21 | 8 | 10 | 1 |
| completo | logistica_B_ejercicio | principal | 45 | 0.333 | 0.383 | 0.258 | 0.500 | 0.202 | 0.229 | 0.000 | 0.767 | 0.292 | 23 | 7 | 15 | 0 |
| con_rezago | logistica_B_ejercicio | principal | 40 | 0.275 | 0.516 | 0.387 | 0.778 | 0.436 | 0.290 | 0.273 | 0.759 | 0.221 | 22 | 7 | 8 | 3 |
| con_rezago | logistica_C-B_ejercicio | principal | 40 | 0.275 | 0.442 | 0.300 | 0.571 | 0.245 | 0.218 | 0.091 | 0.793 | 0.269 | 23 | 6 | 10 | 1 |
| con_rezago | logistica_H_sin_clima | control | 40 | 0.275 | 0.345 | 0.208 | 0.482 | 0.348 | 0.224 | 0.000 | 0.690 | 0.285 | 20 | 9 | 11 | 0 |

Detalle por departamento y por ejercicio en los CSV `*_por_departamento.csv` y `*_por_anio.csv`; hiperparámetros y coeficientes por fold en `*_hiperparametros.csv` y `*_coeficientes.csv`.
