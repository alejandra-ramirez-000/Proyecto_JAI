# Observaciones de la Fase 5: modelos

**Corrida de referencia (v1.1):** `reports/runs/20261030-103735_modelos/`. Todas las cifras provienen de sus CSV: `criterios_*.csv`, `*_metricas.csv`, `*_hiperparametros.csv` y `*_coeficientes.csv`.

**Corridas anteriores (reemplazadas, se conservan para comparación):**

- `reports/runs/20261030-092748_modelos/` (v1.0). Su selección de hiperparámetros en clasificación tenía un defecto, que se describe en la sección "Corrección del criterio de selección".
- `reports/runs/20261030-102243_modelos/` (v1.1 sin semilla en la logística Elastic Net). Su solver `saga` recorre los datos en orden aleatorio y no tenía `random_state`, así que esa familia no era reproducible. La corrida de referencia la fija en 42 y se verificó que dos ejecuciones dan diferencia 0,0 en todas las métricas y predicciones. Los modelos principales, los controles y la regresión no cambian.

**Estado:** borrador para revisión por otra persona del equipo.

## Resultado principal

**Ningún modelo climático principal cumple los criterios de la sección 20.** Con la resolución disponible (45 departamento–ejercicio, 9 años), las variables agroclimáticas y el Chill Index no aportan capacidad predictiva fuera de muestra por encima de los baselines ni de la historia propia de cada departamento.

Es un resultado válido según la especificación (secciones 21 y 34): "se reportan resultados negativos si el modelo no supera baselines". La conclusión es la misma con el criterio v1.0, con el v1.1 y con hiperparámetros fijos.

## Regresión: intensidad ganadera

El cambio v1.1 no afecta a la regresión: las métricas son idénticas a las de v1.0.

| Modelo | Conjunto | MAE (UG/ha) | Frente al mejor baseline | Frente al control sin clima |
|---|---|---|---|---|
| R1 promedio departamental | completo | 0,0263 | — | — |
| Ridge A (clima básico) | completo | 0,0269 | −2,3 % | — |
| Ridge B (Chill Index) | completo | 0,0286 | −9,0 % | — |
| R2 persistencia | con rezago | 0,0195 | — | — |
| Ridge H (solo rezago, control) | con rezago | 0,0189 | +2,9 % | — |
| Ridge C-A (clima + rezago) | con rezago | 0,0210 | −7,9 % | −11,2 % |
| Ridge C-B (CI + rezago) | con rezago | 0,0210 | −7,7 % | −10,9 % |

- **El clima empeora la predicción.** Agregar clima al rezago empeora el MAE en alrededor de 11 % frente al control sin clima.
- **El mejor modelo no tiene clima.** Es el control H, y su mejora sobre la persistencia (2,9 %) está por debajo del umbral de 5 % y desaparece al quitar 2018 (skill sin 2018: −4,1 %).
- **Los coeficientes climáticos son mínimos.** En Ridge C-B, el efecto de cada variable climática es de alrededor de 0,001–0,008 UG/ha por desvío estándar, contra alrededor de 0,13 del rezago. Solo `dias_ci_ge_1200` mantiene el signo (negativo) en los 8 folds.
- **Grilla:** Ridge elige `alpha = 0,1`, el extremo menos regularizado de la grilla, en 7 de 8 folds. No se amplió la grilla, como pide la sección 17.1.
- **Sensibilidad:** `ridge_C-A_jul_oct` obtiene MAE 0,0188, prácticamente igual al control H (0,0189), y queda 3,6 % por debajo de R2. Está bajo el umbral de mejora débil y es una de 66 especificaciones evaluadas.

## Clasificación: mortalidad ovina elevada

| Modelo | Conjunto | BA v1.0 | **BA v1.1** | IC 95 % (v1.1) | AUC concatenado (v1.1) | AUC promedio de folds (v1.1) |
|---|---|---|---|---|---|---|
| C1 / C3 | ambos | 0,50 | 0,50 | — | 0,50 | 0,50 |
| C2 persistencia de riesgo | con rezago | 0,73 | **0,73** | 0,50–0,94 | 0,73 | 0,65 |
| Logística H (control sin clima) | con rezago | 0,34 | **0,67** | 0,43–0,84 | 0,58 | 0,60 |
| Logística A | completo | 0,42 | 0,58 | 0,48–0,71 | 0,50 | 0,62 |
| Logística A | con rezago | 0,49 | 0,49 | 0,32–0,69 | 0,45 | 0,42 |
| Logística B | completo | 0,38 | 0,32 | 0,18–0,55 | 0,31 | 0,43 |
| Logística B | con rezago | 0,52 | 0,32 | 0,21–0,53 | 0,19 | 0,29 |
| Logística C-A | con rezago | 0,41 | 0,50 | 0,39–0,63 | 0,43 | 0,50 |
| Logística C-B | con rezago | 0,44 | 0,37 | 0,32–0,44 | 0,30 | 0,33 |

- **El control sin clima recupera su nivel real** (0,67, frente a 0,70 con hiperparámetros fijos y 0,73 de C2).
- **Agregar clima al rezago empeora la clasificación:** BA de 0,67 sin clima, 0,50 con clima básico (C-A) y 0,37 con el Chill Index (C-B).
- **Los conjuntos del Chill Index (B, C-B) quedan por debajo del azar en todas las rondas.** La relación que aprenden en unos años se invierte en el año que se deja afuera.
- **El caso más cercano a una señal es la logística A en el panel completo:**
  - BA 0,58: supera a C1/C3 por 0,08 y sigue superándolos al quitar cualquier año (diferencia mínima 0,05).
  - Su AUC es 0,50, así que no ordena mejor que el azar.
  - Sus signos son inestables: el signo mayoritario aparece en el 56 % de los folds.
  - Mejora solo en 1 de 5 departamentos.
  - No cumple los criterios.
- **Calibración:** ningún modelo mejora el Brier de los baselines (0,229 en el panel completo, 0,199 con rezago).

### Hallazgos aislados (no son evidencia)

- **La logística Elastic Net (secundaria) es inestable.** Sin semilla, su balanced accuracy variaba hasta 0,36 entre ejecuciones.
  - Ejemplo: `logistica_en_B_ejercicio` en el panel completo dio BA 0,72 en una ejecución y 0,50 con la semilla fija.
  - Con semilla fija, su AUC concatenado (0,72) sigue lejos de su AUC promedio de folds (0,50). Es el artefacto de concatenación de la sección 18.3 en la dirección opuesta: las diferencias de escala entre folds **inflan** el AUC global.
  - Sus resultados no deben leerse como evidencia.
- **`arbol_B_ejercicio`**, que en v1.0 daba BA 0,72, en v1.1 da 0,52. El resultado depende del criterio de selección.

Con 66 especificaciones evaluadas, estos valores aislados son esperables por azar. La sección 17.2 impide usarlos como única evidencia.

## Corrección del criterio de selección (v1.0 → v1.1)

Está registrada en el historial de la especificación (sección 39) y en la sección 18.2.

**Problema en v1.0.** Los hiperparámetros de clasificación se elegían por balanced accuracy sobre las predicciones internas, con desempate por la opción más regularizada.
- En muchos folds todos los candidatos empataban en 0,5.
- El desempate elegía `C = 0,01` sin ponderar clases, un modelo casi constante con probabilidad ≈ 0,29 para todos los casos.
- Resultado: el control H quedó en BA 0,34 y varios AUC concatenados cayeron muy por debajo de 0,5.

**Corrección en v1.1.** La selección pasa a usar la log-loss balanceada (las dos clases pesan igual), con desempate por balanced accuracy.
- Es continua, así que casi no hay empates.
- Penaliza al modelo constante: predecir siempre la prevalencia tiene una pérdida mayor que predecir 0,5.

**Transparencia.** El cambio se decidió **después** de ver la corrida v1.0, y por eso se conservan las dos corridas. La corrección no cambia la conclusión: en ninguna versión el clima cumple los criterios.

**Diagnóstico agregado.** Se agregó el AUC promedio de los folds con ambas clases. Sirve para detectar cuándo el AUC concatenado está distorsionado, hacia abajo (v1.0) o hacia arriba (`logistica_en_B_ejercicio`: 0,72 concatenado frente a 0,50 por fold).

## Ronda exploratoria registrada: hiperparámetros fijos

Corrida: `reports/runs/20261030-102307_exploratoria_hiperparametros_fijos/`. Se reproduce con `python -m src.models.run_exploratory`. Sus resultados son idénticos a los de la primera ejecución (`20261030-101359_…`), porque con un solo candidato el criterio de selección no interviene.

**Es exploratoria.** Se definió después de ver la corrida v1.0 y no reemplaza a la corrida de referencia.

Configuración:

- Ridge con `alpha = 1`.
- Logística con `C = 1` y `class_weight="balanced"`.

**Clasificación** (panel con rezago, 40 obs.):

| Modelo | BA v1.1 (grilla) | BA con C fijo | IC 95 % (C fijo) | AUC concatenado (C fijo) | AUC promedio de folds (C fijo) |
|---|---|---|---|---|---|
| C2 persistencia de riesgo | 0,73 | 0,73 | 0,50–0,94 | 0,73 | 0,65 |
| H: solo rezago (control) | 0,67 | 0,70 | 0,42–0,89 | 0,60 | 0,71 |
| A: clima básico | 0,49 | 0,51 | 0,40–0,70 | 0,48 | 0,46 |
| B: Chill Index | 0,32 | 0,32 | 0,21–0,53 | 0,28 | 0,38 |
| C-A: clima básico + rezago | 0,50 | 0,54 | 0,40–0,68 | 0,53 | 0,50 |
| C-B: Chill Index + rezago | 0,37 | 0,33 | 0,21–0,47 | 0,28 | 0,33 |

- **v1.1 y C fijo coinciden.** Con el criterio v1.1, la selección por grilla da resultados muy parecidos a fijar `C = 1`: la grilla ya no introduce el artefacto de v1.0.
- **Regresión:** con `alpha = 1` todos los Ridge empeoran respecto de la grilla. Ejemplos: A en el panel completo pasa de MAE 0,0269 a 0,0313; el control H, de 0,0189 a 0,0197.

## Por qué el clima no aporta (interpretación)

Es consistente con el EDA (`reports/eda_observaciones.md`):

- **La asociación viene de shocks comunes de año.** La relación clima–mortalidad se explica sobre todo por años que afectan a los cinco departamentos a la vez. Con Leave-One-Year-Out hay que predecir ese shock común a partir de solo 8 años de entrenamiento; la información climática efectiva equivale a 8–9 observaciones.
- **La intensidad está dominada por el nivel estructural de cada departamento y su persistencia.** El clima del ejercicio no agrega información medible.
- **Hay límites del dato** (sección 32):
  - mortalidad anual sin fecha;
  - mortalidad por especie y no de corderos;
  - una sola estación por departamento;
  - un denominador al cierre que cae en 2024–2025.

## Criterios de la sección 20 (corrida v1.1)

| Criterio | Regresión (Ridge A/B/C-A/C-B) | Clasificación (logística A/B/C-A/C-B) |
|---|---|---|
| 1. Supera a todos los baselines | No (0 de 6) | Solo logística A en el panel completo (1 de 6) |
| 2. Fuera de muestra | Sí (por construcción) | Sí |
| 3. No depende de un solo año | No | Solo logística A en el panel completo |
| 4. Signos estables (≥ 80 % de los folds) | Solo A (completo y con rezago) y C-A | Ninguno (máximo 78 %) |
| 5. Mejora en ≥ 3 de 5 departamentos | Solo C-A (3 de 5) | No (máximo 1 de 5) |
| 6. Se sostiene en alguna sensibilidad | Mayormente no | Solo en el panel completo |
| 7. Sin fuga | Sí (verificado por tests) | Sí |
| **Valor predictivo** | **No (ningún modelo)** | **No (ningún modelo)** |

Afirmaciones permitidas (sección 33):

- "Los modelos climáticos no mejoran a los baselines en validación fuera de muestra."
- "La historia de cada departamento (persistencia) es el mejor predictor disponible."

## Pendientes

1. ~~Registrar la ronda exploratoria con hiperparámetros fijos.~~ Registrada.
2. ~~Corregir el criterio de selección de clasificación.~~ Corregido en v1.1.
3. Sensibilidad del denominador de mortalidad con `stock_ovino_pd_pf` (propuesta en el EDA, todavía no corrida).
4. Revisión por otra persona del equipo.
