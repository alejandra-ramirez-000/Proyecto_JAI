# Observaciones del análisis exploratorio

Interpretación escrita de `reports/eda.md`. Las cifras provienen de las tablas en `reports/tables/eda_*.csv`, generadas por `python -m src.reporting.eda`. Si se regenera el EDA y cambian, hay que revisar este documento.

**Estado:** borrador para revisión por otra persona del equipo (criterio de salida de la Fase 3).

Este análisis es descriptivo y observacional. No se usa para elegir variables ni modelos: los conjuntos A, B y C de la sección 13.6 y las grillas de la sección 17 quedan como están.

## 1. Calidad y cobertura climática

- Las cinco estaciones tienen cobertura de al menos 99,2 % en todos los ejercicios 2017–2025, tanto en la ventana completa como en julio–octubre (figuras 1 y 2).
- Los faltantes son casi todos de viento: 18 días en total. El máximo es Treinta y Tres en 2025, con 6 días.
- No hace falta ninguna imputación.

## 2. Objetivos

**Intensidad ganadera (figura 3).**
- Hay dos grupos separados: Canelones y Colonia (alrededor de 1,0–1,2 UG/ha) y Salto, Tacuarembó y Treinta y Tres (alrededor de 0,7 UG/ha).
- Cambia muy poco de un año a otro. La correlación con el ejercicio anterior es 0,99 global y 0,62 dentro de cada departamento.
- Canelones muestra una tendencia creciente entre 2019 y 2024.
- Esto anticipa que el baseline de persistencia (R2) va a ser difícil de superar.

**Mortalidad ovina (figuras 4 a 6).**
- El nivel difiere mucho entre departamentos: la mediana va de 50 por mil en Salto a 82 en Canelones.
- Hay un patrón común muy marcado: los cinco departamentos bajan en 2021–2023 y suben en 2024–2025.
- La correlación con la mortalidad del ejercicio anterior es 0,77 global y 0,43 dentro de cada departamento.

**Stock y muertes (figura 5).**
- El stock ovino cae en todos los departamentos con stock relevante. Salto pasa de unos 1,3 millones a 1,0 millón, y Tacuarembó de 625 mil a 397 mil.
- Como el denominador es la existencia al cierre, parte de la suba de la tasa en 2024–2025 puede venir del stock que cae y no solo de las muertes.
- Ejemplo: en Tacuarembó, las muertes de 2025 son parecidas a las de 2024, pero el stock es menor.

## 3. Clima y Chill Index

**Días en categorías de riesgo (figura 7).**
- Colonia, Canelones y Treinta y Tres acumulan más días con CI ≥ 900; Salto, menos.
- El ejercicio 2023 tiene la menor exposición en casi todos los departamentos: 24 días con CI ≥ 1000 de promedio, contra 38–56 en los demás años.
- 2023 es también el ejercicio más seco del período en los cinco departamentos: 795 mm de promedio, contra 1.030–1.773 mm en los demás.

## 4. Relación clima–mortalidad

Hay que leer tres tipos de correlación (figura 11):

| Tipo | Qué mide | Ejemplo: días con CI ≥ 1000 frente a mortalidad |
|---|---|---|
| Global | Mezcla diferencias entre regiones y entre años | +0,46 |
| Intra-departamento | Variación entre años dentro de cada departamento | +0,38 |
| Intra-departamento y año | Quita además el shock común de cada año | +0,11 |

Hallazgos principales:

1. **La señal climática está concentrada en shocks comunes de año.** Al descontar la media de cada ejercicio, las correlaciones del CI con la mortalidad caen de alrededor de 0,4 a alrededor de 0,1:
   - días con CI ≥ 1200: de 0,41 a 0,13;
   - percentil 95 del CI: de 0,38 a −0,05.

   Los años con más exposición al frío coinciden con los años de más mortalidad en todos los departamentos a la vez, pero dentro de un mismo año, el departamento con más CI no es el de más mortalidad. En términos prácticos, la información climática equivale a unos **9 años**, no a 45 observaciones independientes.
2. **La precipitación muestra la asociación más fuerte:** 0,54 intra-departamento y 0,35 tras descontar el año.
   - Es positiva en los cinco departamentos (n = 9 cada uno): de 0,20 en Treinta y Tres a 0,80 en Salto (figura 8).
   - La precipitación entra en el CI, pero también puede reflejar otros mecanismos, como las condiciones de pastura o sanitarias.
   - No se puede atribuir la asociación al frío.
3. **La relación varía entre departamentos** (figuras 9 y 10):
   - Para días con CI ≥ 1000, va de 0,05 en Canelones a 0,86 en Salto.
   - Con 9 puntos por departamento, estas diferencias son muy inciertas.
4. **La global puede engañar:** en 4 de 24 pares variable–objetivo la correlación global y la intra-departamento tienen signo opuesto.
   - Ejemplo: temperatura frente a mortalidad da −0,63 global y +0,11 intra-departamento.
   - La global refleja que los departamentos del norte, más cálidos, tienen menos mortalidad; no muestra un efecto de la temperatura en el tiempo.
5. **Para intensidad**, las correlaciones con el clima son negativas y moderadas (alrededor de −0,3 a −0,44). Pero la intensidad tiene tendencia y es muy persistente, así que estas asociaciones pueden confundirse con tendencias de largo plazo.

## 5. Ejercicio completo frente a julio–octubre (figura 13)

- Para la mortalidad, la ventana julio–octubre da correlaciones de igual signo pero algo más débiles que el ejercicio completo, en casi todas las variables del CI.
- Para la intensidad, julio–octubre da correlaciones algo más fuertes.
- Siguiendo la sección 10.2, la elección entre ventanas se decide por validación fuera de muestra y no por esta figura.

## 6. Años extremos (figura 12)

- Hay 15 combinaciones departamento–ejercicio con |z| ≥ 1,5 en algún objetivo, en días con CI ≥ 1000 o en precipitación.
- Mortalidad alta:
  - Canelones 2019 (z = +1,7);
  - Colonia 2025 (+1,8);
  - Salto 2024 (+1,6);
  - Treinta y Tres 2025 (+2,0).
- Mortalidad baja:
  - Tacuarembó 2022 (−1,6);
  - Treinta y Tres 2023 (−1,6).
- 2023 es extremo bajo en exposición al CI en cuatro departamentos.

Para la Fase 5 hay que verificar que una eventual mejora del modelo **no dependa de un único año** (criterio 3 de la sección 20); 2023 y 2024 son los candidatos a revisar.

## 7. Implicancias para la validación (sin elegir modelos)

1. **El efecto año común frente a Leave-One-Year-Out.** En LOYO se deja afuera un año completo, con sus cinco departamentos. El modelo tiene que predecir el shock común de ese año a partir del clima, y solo hay 8 años de entrenamiento para aprenderlo. Esto vuelve la evaluación exigente, y es lo que corresponde.
2. **Persistencia de la intensidad.** El baseline de persistencia (R2) parte con una correlación de 0,99. Cualquier mejora del clima sobre él va a ser pequeña en términos absolutos.
3. **Denominador de la mortalidad.** Conviene revisar como sensibilidad la tasa con `stock_ovino_pd_pf` (ya está en el panel), sobre todo en 2024–2025, cuando el stock cae.
4. **Comparaciones múltiples.** Se exploraron 24 variables por objetivo. Una correlación aislada de 0,3–0,4 es compatible con el azar.

## Pendiente

- La figura 14 (observados frente a predicciones fuera de muestra) se genera en la Fase 5.
- Falta la revisión de este documento por otra persona del equipo.
