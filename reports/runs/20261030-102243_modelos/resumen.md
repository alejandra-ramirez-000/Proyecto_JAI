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
| completo | logistica_A_ejercicio | principal | 0.583 | 0.504 | C1_clase_mayoritaria | 0.500 | 0.083 | True | True | 0.053 | True | 0.556 | 1 | 3 | 4 |  | False | no |
| con_rezago | logistica_A_ejercicio | principal | 0.486 | 0.451 | C2_persistencia_riesgo | 0.732 | -0.246 | False | False | -0.338 | False | 0.500 | 0 | 0 | 4 | -0.188 | False | no |
| con_rezago | logistica_C-A_ejercicio | principal | 0.503 | 0.426 | C2_persistencia_riesgo | 0.732 | -0.229 | False | False | -0.317 | False | 0.750 | 0 | 0 | 4 | -0.171 | False | no |
| completo | logistica_B_ejercicio | principal | 0.317 | 0.307 | C1_clase_mayoritaria | 0.500 | -0.183 | False | False | -0.274 | False | 0.778 | 0 | 3 | 4 |  | False | no |
| con_rezago | logistica_B_ejercicio | principal | 0.320 | 0.194 | C2_persistencia_riesgo | 0.732 | -0.412 | False | False | -0.528 | False | 0.625 | 0 | 0 | 4 | -0.354 | False | no |
| con_rezago | logistica_C-B_ejercicio | principal | 0.371 | 0.301 | C2_persistencia_riesgo | 0.732 | -0.361 | False | False | -0.428 | False | 0.625 | 0 | 0 | 4 | -0.303 | False | no |
| con_rezago | logistica_H_sin_clima | control | 0.674 | 0.580 | C2_persistencia_riesgo | 0.732 | -0.058 | False | False | -0.111 | False |  | 1 | 0 | 0 | 0.000 | False | no aplica (control) |

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

| conjunto | modelo | rol | n | prevalencia | balanced_accuracy | balanced_accuracy_ic95_inf | balanced_accuracy_ic95_sup | roc_auc | roc_auc_promedio_folds | average_precision | recall | especificidad | brier | tn | fp | fn | tp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | C1_clase_mayoritaria | baseline | 45 | 0.333 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.333 | 0.000 | 1.000 | 0.229 | 30 | 0 | 15 | 0 |
| con_rezago | C1_clase_mayoritaria | baseline | 40 | 0.275 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.275 | 0.000 | 1.000 | 0.199 | 29 | 0 | 11 | 0 |
| con_rezago | C2_persistencia_riesgo | baseline | 40 | 0.275 | 0.732 | 0.496 | 0.941 | 0.732 | 0.646 | 0.471 | 0.636 | 0.828 | 0.225 | 24 | 5 | 4 | 7 |
| completo | C3_historial_departamental | baseline | 45 | 0.333 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.333 | 0.000 | 1.000 | 0.229 | 30 | 0 | 15 | 0 |
| con_rezago | C3_historial_departamental | baseline | 40 | 0.275 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.275 | 0.000 | 1.000 | 0.199 | 29 | 0 | 11 | 0 |
| completo | logistica_A_ejercicio | principal | 45 | 0.333 | 0.583 | 0.477 | 0.705 | 0.504 | 0.617 | 0.409 | 0.467 | 0.700 | 0.261 | 21 | 9 | 8 | 7 |
| con_rezago | logistica_A_ejercicio | principal | 40 | 0.275 | 0.486 | 0.319 | 0.686 | 0.451 | 0.417 | 0.357 | 0.455 | 0.517 | 0.287 | 15 | 14 | 6 | 5 |
| con_rezago | logistica_C-A_ejercicio | principal | 40 | 0.275 | 0.503 | 0.387 | 0.634 | 0.426 | 0.500 | 0.281 | 0.455 | 0.552 | 0.288 | 16 | 13 | 6 | 5 |
| completo | logistica_B_ejercicio | principal | 45 | 0.333 | 0.317 | 0.181 | 0.546 | 0.307 | 0.433 | 0.254 | 0.333 | 0.300 | 0.253 | 9 | 21 | 10 | 5 |
| con_rezago | logistica_B_ejercicio | principal | 40 | 0.275 | 0.320 | 0.208 | 0.534 | 0.194 | 0.292 | 0.190 | 0.364 | 0.276 | 0.271 | 8 | 21 | 7 | 4 |
| con_rezago | logistica_C-B_ejercicio | principal | 40 | 0.275 | 0.371 | 0.315 | 0.444 | 0.301 | 0.333 | 0.215 | 0.364 | 0.379 | 0.266 | 11 | 18 | 7 | 4 |
| con_rezago | logistica_H_sin_clima | control | 40 | 0.275 | 0.674 | 0.432 | 0.839 | 0.580 | 0.604 | 0.332 | 0.727 | 0.621 | 0.260 | 18 | 11 | 3 | 8 |

Detalle por departamento y por ejercicio en los CSV `*_por_departamento.csv` y `*_por_anio.csv`; hiperparámetros y coeficientes por fold en `*_hiperparametros.csv` y `*_coeficientes.csv`.
