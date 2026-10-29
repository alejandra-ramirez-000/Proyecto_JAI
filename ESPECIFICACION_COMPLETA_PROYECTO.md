# Especificación completa del proyecto

## Evaluación de la capacidad predictiva del Chill Index sobre la intensidad ganadera y la mortalidad ovina en Uruguay

**Versión:** 1.0  
**Fecha:** 28 de octubre de 2026  
**Estado:** especificación metodológica lista para implementación  
**Propósito del documento:** permitir que cualquier integrante del equipo pueda comprender, implementar, revisar y reproducir el proyecto sin depender de explicaciones orales adicionales.

## Navegación rápida

- [Resumen ejecutivo](#1-resumen-ejecutivo)
- [Idea central](#2-idea-central-del-proyecto)
- [Preguntas y objetivos](#3-preguntas-de-investigación)
- [Alcance](#5-alcance)
- [Fuentes de datos](#6-fuentes-de-datos)
- [Granularidad](#7-granularidad-y-unidad-estadística)
- [Diccionario de datos](#8-diccionario-de-datos-relevante)
- [Calidad de datos](#9-hallazgos-de-calidad-de-datos-ya-verificados)
- [Alineación temporal](#10-alineación-temporal)
- [Chill Index](#11-cálculo-del-chill-index)
- [Objetivos de modelado](#12-construcción-de-los-objetivos)
- [Variables predictoras](#13-variables-predictoras)
- [Preparación del panel](#14-proceso-de-preparación-de-datos)
- [Prevención de fuga](#16-prevención-de-fuga-de-información)
- [Modelos](#17-diseño-de-modelos)
- [Validación](#18-protocolo-de-validación)
- [Métricas y criterios de éxito](#19-métricas)
- [Resultados preliminares](#21-resultados-preliminares-de-la-auditoría)
- [Estructura del repositorio](#24-estructura-recomendada-del-repositorio)
- [Tests](#27-tests-obligatorios)
- [Entregables y plan](#29-entregables)
- [Riesgos](#32-riesgos-y-mitigaciones)
- [Decisiones cerradas](#35-decisiones-metodológicas-cerradas)
- [Referencias](#38-referencias-principales)

---

## 1. Resumen ejecutivo

El proyecto evaluará si las condiciones agroclimáticas, y en particular el **Chill Index** o índice de enfriamiento, aportan información útil para:

1. estimar la **intensidad ganadera departamental**; y
2. identificar ejercicios ganaderos con **mortalidad ovina elevada**.

Se integrarán datos diarios de estaciones agroclimáticas del Instituto Nacional de Investigación Agropecuaria (INIA) con datos anuales de declaraciones DICOSE publicados por el Sistema Nacional de Información Ganadera (SNIG).

El estudio abarcará cinco departamentos:

- Canelones;
- Colonia;
- Salto;
- Tacuarembó; y
- Treinta y Tres.

El período principal será **2017–2025**, definido según el ejercicio ganadero que comienza el 1 de julio del año anterior y finaliza el 30 de junio del año identificado por SNIG. Por ejemplo, el ejercicio 2020 comprende desde el 1 de julio de 2019 hasta el 30 de junio de 2020.

La unidad de análisis será:

> **una combinación departamento–ejercicio ganadero**.

Esto produce un máximo de **45 observaciones independientes**: cinco departamentos por nueve ejercicios ganaderos completos. Aunque los archivos originales contienen cientos de miles de filas, esas filas no representan exposiciones climáticas independientes porque todas las subdivisiones de un mismo departamento y año reciben las mismas variables de la estación asignada.

El proyecto se planteará como una **evaluación de capacidad predictiva**, no como un sistema operacional de alerta. Los modelos deberán demostrar que superan referencias simples —como el promedio histórico departamental o el último valor conocido— antes de afirmar que existe valor predictivo climático.

No se construirá un dashboard. Los resultados se entregarán mediante datasets procesados, código reproducible, métricas, tablas, gráficos y un informe final.

---

## 2. Idea central del proyecto

La variabilidad climática puede modificar la actividad ganadera y generar condiciones adversas para la supervivencia de los ovinos. El frío, el viento y la precipitación aumentan la pérdida potencial de calor de los animales. Esta exposición puede representarse mediante el Chill Index, un índice biometeorológico relacionado con la supervivencia de corderos durante sus primeras 72 horas de vida y con el riesgo para ovinos luego de la esquila.

El proyecto investigará si la exposición climática acumulada durante cada ejercicio ganadero se relaciona con:

- cambios en la cantidad de unidades ganaderas por hectárea;
- cambios en la mortalidad ovina anual declarada; y
- una mayor probabilidad de que la mortalidad ovina supere el nivel históricamente habitual de cada departamento.

La pregunta principal no será “¿podemos entrenar un modelo?”, porque siempre es posible ajustar un algoritmo a una tabla pequeña. La pregunta correcta será:

> **¿Las variables climáticas aportan capacidad predictiva fuera de muestra por encima de la historia propia de cada departamento?**

---

## 3. Preguntas de investigación

### 3.1. Pregunta principal

¿El Chill Index y otras variables agroclimáticas mejoran la predicción anual de intensidad ganadera y mortalidad ovina en los departamentos estudiados?

### 3.2. Preguntas secundarias

1. ¿Qué relación existe entre la cantidad de días con Chill Index elevado y la tasa proxy de mortalidad ovina?
2. ¿La precipitación, la temperatura y el viento aportan información adicional a la contenida en el Chill Index?
3. ¿El desempeño cambia entre departamentos?
4. ¿Un modelo climático supera al promedio histórico departamental?
5. ¿Un modelo climático supera al último valor observado del objetivo?
6. ¿Los resultados se mantienen cuando se deja un año completo fuera del entrenamiento?
7. ¿Las conclusiones cambian al analizar todo el ejercicio ganadero frente al período julio–octubre, utilizado como aproximación a una temporada de mayor sensibilidad de pariciones?

---

## 4. Objetivos

### 4.1. Objetivo general

Evaluar la capacidad predictiva de variables agroclimáticas y del Chill Index sobre la intensidad ganadera y la mortalidad ovina anual en Canelones, Colonia, Salto, Tacuarembó y Treinta y Tres durante los ejercicios ganaderos 2017–2025.

### 4.2. Objetivos específicos

1. Integrar datos climáticos diarios de INIA con datos ganaderos anuales de SNIG.
2. Construir una tabla analítica departamento–ejercicio con una fila por unidad independiente.
3. Calcular el Chill Index diario siguiendo la fórmula publicada por INIA.
4. Construir indicadores anuales de exposición a frío, viento y precipitación.
5. Calcular una medida de intensidad ganadera expresada en unidades ganaderas por hectárea ganadera.
6. Calcular una tasa proxy de mortalidad ovina por cada mil animales.
7. Definir una etiqueta de mortalidad elevada relativa al historial de cada departamento.
8. Entrenar modelos de regresión y clasificación adecuados para una muestra pequeña.
9. Comparar todos los modelos contra baselines simples y difíciles de superar.
10. Aplicar validación temporal, evitando cualquier fuga de información entre años.
11. Documentar las limitaciones de los datos y las afirmaciones que pueden o no realizarse.

---

## 5. Alcance

### 5.1. Alcance geográfico

Se trabajará exclusivamente con los departamentos que tienen una estación de INIA seleccionada para todo el período:

| Código SNIG | Departamento | Estación INIA asignada |
|---:|---|---|
| 2 | Canelones | Las Brujas |
| 4 | Colonia | La Estanzuela |
| 15 | Salto | Salto Grande |
| 18 | Tacuarembó | Tacuarembó La Magnolia |
| 19 | Treinta y Tres | Treinta y Tres Paso de la Laguna |

Para Tacuarembó se utilizará **La Magnolia**. No se utilizará la estación Glencore porque:

- comienza después que las demás estaciones;
- tiene períodos extensos sin observaciones; y
- presenta un porcentaje elevado de valores faltantes en recorrido del viento.

No se deben combinar ambas estaciones de Tacuarembó como si fueran observaciones independientes, porque el objetivo SNIG es único para el departamento y año.

### 5.2. Alcance temporal

- Datos SNIG disponibles: 2016–2025.
- Datos INIA disponibles en el archivo: 1 de enero de 2016 a 17 de marzo de 2026.
- Período principal modelable: ejercicios 2017–2025.
- Cantidad de ejercicios completos: 9.
- Cantidad máxima de observaciones: 45.
- Modelos que utilicen un rezago anual: ejercicios 2018–2025, equivalentes a 40 observaciones.

El ejercicio 2016 no se utilizará como observación principal porque requeriría clima desde julio de 2015 y el archivo INIA comienza en enero de 2016.

### 5.3. Alcance analítico

El proyecto incluye:

- auditoría de calidad de datos;
- integración de fuentes;
- ingeniería de variables;
- análisis exploratorio;
- modelos de regresión;
- modelos de clasificación;
- validación temporal;
- interpretación y comparación contra baselines;
- documentación reproducible; y
- elaboración de un informe final.

### 5.4. Fuera de alcance

No forman parte del alcance:

- dashboard o aplicación web;
- predicción a nivel de establecimiento individual;
- predicción diaria de muertes;
- identificación de la causa clínica de muerte;
- estimación causal del efecto del clima;
- alerta operacional en tiempo real;
- extrapolación a departamentos sin estación INIA asignada;
- modelos de redes neuronales o aprendizaje profundo;
- uso de datos lecheros, tenencia de tierra o categorías animales detalladas; y
- atribución de toda la mortalidad ovina al Chill Index.

---

## 6. Fuentes de datos

### 6.1. Inventario de archivos activos

| Archivo | Formato | Filas aproximadas | Cobertura | Uso |
|---|---|---:|---|---|
| `data/raw/INIA.csv` | CSV separado por comas | 21.402 | 2016-01-01 a 2026-03-17 | Variables climáticas diarias y cálculo del Chill Index |
| `data/raw/SNIG/DatosAnimales.csv` | CSV separado por `;` | 677.035 | 2016–2025 | Mortalidad, existencias y cantidad de tenedores por especie |
| `data/raw/SNIG/DatosGenerales.csv` | CSV separado por `;` | 315.536 | 2016–2025 | Unidades ganaderas y superficie ganadera |
| `data/raw/SNIG/Catalogos/Departamentos.csv` | CSV separado por `;` | 19 | Catálogo | Traducción de códigos de departamento |
| `data/raw/SNIG/Catalogos/Especies.csv` | CSV separado por `;` | 7 | Catálogo | Traducción de códigos de especie |

Los archivos de `data/raw` deben considerarse **inmutables**. No se deben editar, reordenar, sobrescribir ni guardar versiones transformadas dentro de esa carpeta.

### 6.2. Archivos descartados

Los archivos que no se utilizarán se encuentran en:

`data/raw/SNIG/No usar/`

Allí se movieron:

- animales detallados por categoría;
- producción de leche;
- producción de leche en establecimiento;
- tenencias de tierra;
- usos de tierra; y
- catálogos exclusivos o no requeridos por el panel final.

La carpeta `No usar` permite recuperar los archivos si cambia el alcance, pero los scripts del proyecto no deben leerla de manera automática.

### 6.3. Fuentes institucionales de referencia

- INIA, metodología y umbrales del Chill Index:  
  <https://inia.uy/gras/Aplicaciones_y_recursos/Prevision%20Corderos>
- INIA, descripción de variables agroclimáticas y unidad del recorrido del viento:  
  <https://gras.inia.uy/gras/es/ConsultasWebDBC/consulta_bdagroclima/>
- MGAP/SNIG, declaración jurada anual DICOSE:  
  <https://www.gub.uy/tramites/presentacion-declaracion-jurada-dicose>
- Catálogo Nacional de Datos Abiertos, recursos SNIG:  
  <https://catalogodatos.gub.uy/es/dataset/mgap-datos-preliminares-basados-en-la-declaracion-jurada-de-existencias-dicose-snig-2024>

---

## 7. Granularidad y unidad estadística

### 7.1. Granularidad original de SNIG

Los archivos de SNIG contienen combinaciones de:

- año;
- departamento;
- seccional policial;
- área de supervisión;
- área de enumeración;
- actividad;
- giro;
- naturaleza jurídica;
- estrato;
- especie; y
- otras clasificaciones administrativas.

Estas filas son agregados de declaraciones y no establecimientos individuales identificables.

### 7.2. Granularidad climática disponible

INIA aporta una serie diaria por estación. Para este proyecto se asigna una estación a cada departamento. Por lo tanto, todos los registros internos de un mismo departamento y ejercicio reciben la misma exposición climática agregada.

### 7.3. Unidad final obligatoria

La unidad final debe ser:

```text
DepartamentoCodigo + AnioEjercicio
```

Debe existir exactamente una fila por combinación.

No se permite entrenar modelos con las 40.418 filas ovinas originales asignándoles repetidamente el mismo clima departamental. Eso produciría pseudorreplicación, inflaría artificialmente el tamaño de muestra y generaría métricas demasiado optimistas.

---

## 8. Diccionario de datos relevante

### 8.1. `DatosAnimales.csv`

| Columna | Uso | Tratamiento |
|---|---|---|
| `ID` | No usar | Identificador de fila de publicación; no es una entidad ganadera |
| `Anio` | Clave temporal | Convertir a entero |
| `DepartamentoCodigo` | Clave geográfica | Filtrar códigos 2, 4, 15, 18 y 19 |
| `SeccionalPolicialCodigo` | No usar en el modelo final | Conservar solo durante auditoría |
| `AreaSupervision` | No usar en el modelo final | Conservar solo durante auditoría |
| `AreaEnumeracion` | No usar en el modelo final | Conservar solo durante auditoría |
| `ActividadCodigo` | Excluir | No es necesaria tras la agregación departamental |
| `GiroCodigo` | Excluir | No es necesaria tras la agregación departamental |
| `NaturalezaJuridicaCodigo` | Excluir | No es necesaria tras la agregación departamental |
| `EstratoCodigo` | Excluir | No es necesaria tras la agregación departamental |
| `EspecieCodigo` | Filtro | Utilizar únicamente `2 = OVINOS` |
| `AnimalesPorEspecieConsumoPD_AD` | Descriptiva opcional | No usar como predictor principal |
| `AnimalesPorEspecieNacimientosPD_AD` | Descriptiva opcional | No usar como predictor principal por posible simultaneidad con el objetivo |
| `AnimalesPorEspecieMortandadPD_AD` | Numerador del objetivo | Sumar por departamento y ejercicio |
| `CantidadTenedoresPorEspecie` | Descriptiva | Sumar para controles de calidad; no usar inicialmente como predictor |
| `AnimalesPorEspeciePD_AD` | Denominador principal | Sumar por departamento y ejercicio |
| `AnimalesPorEspeciePD_PF` | Sensibilidad | Conservar para comparar denominadores, no mezclar con el principal |
| `EspecializacionMGAPCodigo` | Excluir | 100 % nula entre 2016 y 2021 |
| `TipoProduccionMGAPCodigo` | Excluir | 100 % nula entre 2016 y 2021 |

### 8.2. `DatosGenerales.csv`

| Columna | Uso | Tratamiento |
|---|---|---|
| `ID` | No usar | Identificador de fila |
| `Anio` | Clave temporal | Convertir a entero |
| `DepartamentoCodigo` | Clave geográfica | Filtrar códigos seleccionados |
| `Superficie` | Control descriptivo | Sumar por departamento y ejercicio |
| `UnidadesGanaderas` | Numerador del objetivo de regresión | Convertir decimal con coma y sumar |
| `SuperficieGanadera` | Denominador del objetivo de regresión | Convertir decimal con coma y sumar |
| `CantidadTenedores` | Control descriptivo | Sumar por departamento y ejercicio |
| `EspecializacionMGAPCodigo` | Excluir | 100 % nula entre 2016 y 2021 |
| `TipoProduccionMGAPCodigo` | Excluir | 100 % nula entre 2016 y 2021 |

Las demás columnas categóricas deben excluirse del modelo final una vez verificada la agregación.

### 8.3. `INIA.csv`

| Columna | Unidad | Uso |
|---|---|---|
| `Anio` | año calendario | Construcción de fecha y ejercicio |
| `Mes` | 1–12 | Construcción de fecha y ventanas |
| `Dia` | día del mes | Construcción de fecha |
| `EstacionAgr` | texto | Asignación estación–departamento |
| `TempAireMedia` | °C | Temperatura media diaria del aire |
| `PrecipAcum` | mm/día | Precipitación acumulada diaria |
| `RecorridoViento` | km/día | Recorrido horizontal diario a dos metros de altura |

El resto de las variables climáticas puede utilizarse para análisis descriptivo, pero no debe incorporarse indiscriminadamente al modelo. Con 45 observaciones, la cantidad de predictores debe mantenerse muy reducida.

---

## 9. Hallazgos de calidad de datos ya verificados

1. `DatosAnimales.csv` contiene 677.035 filas y cubre 2016–2025.
2. `DatosGenerales.csv` contiene 315.536 filas y cubre 2016–2025.
3. En los cinco departamentos existen 40.418 filas originales correspondientes a ovinos.
4. Existen las 50 combinaciones departamento–año entre 2016 y 2025.
5. Al alinear ejercicios completos con INIA quedan 45 combinaciones utilizables entre 2017 y 2025.
6. No se detectaron duplicados exactos en las claves dimensionales completas de `DatosAnimales.csv` ni `DatosGenerales.csv`.
7. La mortalidad ovina no presenta valores nulos ni negativos en el subconjunto estudiado.
8. `EspecializacionMGAPCodigo` y `TipoProduccionMGAPCodigo` están completamente vacías entre 2016 y 2021 y completas desde 2022.
9. Esas dos columnas deben excluirse; no se deben imputar como “desconocido”.
10. Las cinco estaciones seleccionadas tienen cobertura diaria prácticamente completa para 2017–2025.
11. La estación Tacuarembó Glencore no tiene calidad suficiente para reemplazar o complementar La Magnolia.
12. El archivo INIA no presenta duplicados estación–fecha.

Estos resultados deben volver a verificarse automáticamente en el pipeline. No deben quedar únicamente documentados como una observación manual.

---

## 10. Alineación temporal

### 10.1. Regla del ejercicio ganadero

Para cada fecha diaria de INIA:

```text
si mes <= 6: AnioEjercicio = año calendario
si mes >= 7: AnioEjercicio = año calendario + 1
```

Ejemplos:

| Fecha INIA | `AnioEjercicio` |
|---|---:|
| 2020-03-15 | 2020 |
| 2020-06-30 | 2020 |
| 2020-07-01 | 2021 |
| 2020-10-20 | 2021 |
| 2021-06-30 | 2021 |

### 10.2. Ventanas climáticas

Se construirán dos ventanas:

1. **Ejercicio completo:** 1 de julio a 30 de junio.
2. **Ventana sensible julio–octubre:** utilizada como análisis de sensibilidad por su proximidad conceptual a períodos de parición, sin afirmar que todas las pariciones ocurren allí.

La ventana julio–octubre no debe reemplazar automáticamente al ejercicio completo. Ambas deben compararse y la elección final debe justificarse con validación fuera de muestra.

### 10.3. Rezagos

Los valores históricos se construirán por departamento:

```text
intensidad_lag1(d, y) = intensidad(d, y - 1)
mortalidad_lag1(d, y) = tasa_mortalidad(d, y - 1)
```

No se puede rellenar el primer rezago con cero ni con un promedio futuro. Los modelos que utilicen rezagos comenzarán en 2018.

---

## 11. Cálculo del Chill Index

### 11.1. Conversión del viento

INIA informa `RecorridoViento` en kilómetros por día. El Chill Index requiere velocidad media diaria en metros por segundo.

La conversión es:

```text
VV = RecorridoViento / 86,4
```

Justificación:

```text
1 km/día = 1.000 m / 86.400 s = 1 / 86,4 m/s
```

### 11.2. Fórmula

La fórmula publicada por INIA es:

```text
R = 418 × (1 - exp(-0,04 × P))

CI = (11,7 + 3,1 × sqrt(VV)) × (40 - Ta) + 481 + R
```

La expresión anterior conserva la notación decimal utilizada en la documentación en español. En Python debe implementarse con punto decimal:

```python
rain_term = 418 * (1 - np.exp(-0.04 * precipitation_mm))
chill_index = (
    (11.7 + 3.1 * np.sqrt(wind_speed_ms))
    * (40 - mean_air_temperature_c)
    + 481
    + rain_term
)
```

Donde:

- `CI`: pérdida potencial de calor, en kJ/m²/h;
- `VV`: velocidad media diaria del viento, en m/s a dos metros;
- `Ta`: temperatura media diaria del aire, en °C; y
- `P`: precipitación total diaria, en mm.

### 11.3. Política de faltantes

Si falta temperatura, viento o precipitación, el Chill Index del día debe quedar como faltante.

No se permite:

- reemplazar viento faltante por cero;
- reemplazar precipitación faltante por cero sin evidencia de que significa “no llovió”;
- calcular CI con una entrada ausente; ni
- ocultar faltantes mediante `fillna(0)`.

Como la cobertura es muy alta, la regla inicial será excluir el día incompleto del agregado y registrar la cantidad de días válidos. Un ejercicio solo podrá modelarse si posee al menos el 95 % de los días esperados con CI calculable.

### 11.4. Categorías oficiales del Chill Index

| Chill Index | Interpretación ambiental |
|---:|---|
| `< 900` | Sin riesgo |
| `900–<1000` | Riesgo bajo |
| `1000–<1100` | Riesgo medio |
| `1100–<1200` | Riesgo alto |
| `>= 1200` | Condiciones críticas |

Estos umbrales describen riesgo ambiental para corderos recién nacidos y ovinos pos-esquila. No son umbrales oficiales de mortalidad anual de SNIG.

### 11.5. Validaciones unitarias del CI

El código debe probar como mínimo que:

1. al aumentar el viento, manteniendo todo lo demás constante, aumenta el CI;
2. al disminuir la temperatura, aumenta el CI;
3. al aumentar la precipitación, aumenta el CI;
4. con precipitación cero, el término `R` es cero;
5. el resultado es nulo si falta cualquier entrada obligatoria; y
6. la conversión de 86,4 km/día produce exactamente 1 m/s.

---

## 12. Construcción de los objetivos

### 12.1. Objetivo de regresión: intensidad ganadera

La intensidad se calculará después de sumar numerador y denominador:

```text
IntensidadGanadera(d, y) =
    SUM(UnidadesGanaderas[d, y])
    / SUM(SuperficieGanadera[d, y])
```

Unidad:

```text
unidades ganaderas por hectárea ganadera (UG/ha)
```

Reglas:

- No calcular el promedio de ratios por fila.
- No dividir cada fila y luego sumar.
- Si la superficie ganadera agregada es cero, el resultado debe quedar como no disponible.
- Verificar que unidades ganaderas y superficie ganadera no sean negativas.
- Conservar ambos componentes agregados en el dataset procesado para auditoría.

En la auditoría preliminar, la intensidad observada se encontró aproximadamente entre 0,68 y 1,23 UG/ha.

### 12.2. Objetivo continuo de mortalidad ovina

Se utilizará una tasa proxy:

```text
TasaMortalidadOvina1000(d, y) =
    1.000 × SUM(AnimalesPorEspecieMortandadPD_AD[d, y])
    / SUM(AnimalesPorEspeciePD_AD[d, y])
```

La tasa debe denominarse **tasa proxy de mortalidad ovina por mil** y no “probabilidad individual de muerte”.

Limitaciones del indicador:

- el numerador resume eventos del ejercicio;
- el denominador es una existencia declarada al cierre y no el promedio de animales expuestos durante todo el año;
- la mortalidad es por especie, no exclusivamente de corderos;
- no se conoce la fecha exacta de cada muerte; y
- no se conoce la causa de muerte.

En la auditoría preliminar, la tasa agregada se encontró aproximadamente entre 31 y 112 muertes por cada mil ovinos, según departamento y ejercicio.

### 12.3. Objetivo de clasificación: mortalidad elevada

La clasificación será relativa al historial de cada departamento.

En cada partición de validación:

1. utilizar únicamente los años de entrenamiento;
2. calcular el percentil 75 de `TasaMortalidadOvina1000` para cada departamento;
3. asignar `1 = mortalidad elevada` si la tasa observada supera ese percentil; y
4. asignar `0 = mortalidad no elevada` en caso contrario.

Formalmente:

```text
umbral_d = Q75(tasa_mortalidad del departamento d en entrenamiento)

MortalidadElevada(d, y) = 1 si tasa(d, y) > umbral_d
                         0 en otro caso
```

### Regla crítica contra fuga de información

El percentil no puede calcularse una única vez usando todo el período antes de la validación. Debe recalcularse dentro de cada conjunto de entrenamiento.

### Regla contra circularidad

No se debe definir la etiqueta de mortalidad elevada a partir del Chill Index. El Chill Index es un predictor ambiental. Si la etiqueta se construyera con el mismo índice, el modelo solo aprendería una regla definida de antemano y no estaría prediciendo mortalidad observada.

---

## 13. Variables predictoras

### 13.1. Variables obligatorias de identificación

- `DepartamentoCodigo`;
- `Departamento`;
- `AnioEjercicio`;
- `EstacionAgr`.

### 13.2. Variables climáticas básicas

Por ejercicio y departamento:

- temperatura media del ejercicio;
- temperatura media julio–octubre;
- precipitación total del ejercicio;
- precipitación total julio–octubre;
- velocidad media del viento del ejercicio;
- velocidad media del viento julio–octubre;
- cantidad de días climáticos válidos; y
- porcentaje de cobertura climática.

### 13.3. Variables del Chill Index

Por ejercicio y departamento:

- CI medio;
- CI máximo;
- percentil 95 del CI;
- cantidad de días con `CI >= 900`;
- cantidad de días con `CI >= 1000`;
- cantidad de días con `CI >= 1100`;
- cantidad de días con `CI >= 1200`;
- proporción de días con `CI >= 1000`;
- proporción de días con `CI >= 1200`;
- máxima cantidad de días consecutivos con `CI >= 1000`; y
- máxima cantidad de días consecutivos con `CI >= 1200`.

Las mismas variables pueden calcularse para julio–octubre como análisis de sensibilidad.

### 13.4. Variables históricas

- intensidad ganadera del ejercicio anterior;
- tasa proxy de mortalidad del ejercicio anterior;
- stock ovino del ejercicio anterior; y
- cantidad de tenedores ovinos del ejercicio anterior.

Los valores simultáneos del mismo ejercicio no deben usarse como predictores si contienen información generada al mismo tiempo que el objetivo y no estaría disponible al momento de pronosticar.

### 13.5. Efecto departamento

El departamento debe incluirse como variable categórica o efecto fijo para controlar diferencias estructurales persistentes.

No se debe representar el código numérico del departamento como una variable continua. Los códigos 2, 4, 15, 18 y 19 son identificadores, no cantidades ordenadas.

### 13.6. Conjuntos reducidos de variables

Debido al tamaño de muestra, no se entrenará un modelo con todas las variables simultáneamente. Se compararán especificaciones predefinidas:

#### Conjunto A: clima básico

- temperatura media;
- precipitación total;
- viento medio; y
- departamento.

#### Conjunto B: exposición Chill Index

- días con CI >= 1000;
- días con CI >= 1200;
- CI máximo; y
- departamento.

#### Conjunto C: clima más historia

- variables del conjunto A o B;
- rezago del objetivo; y
- departamento.

No se deben combinar conjuntos o agregar variables después de observar cuál mejora el resultado sin registrar que se trata de exploración.

---

## 14. Proceso de preparación de datos

### 14.1. Carga

1. Cargar `DatosAnimales.csv` con separador `;` y codificación `utf-8-sig`.
2. Cargar `DatosGenerales.csv` con separador `;` y codificación `utf-8-sig`.
3. Cargar los catálogos con separador `;`.
4. Cargar `INIA.csv` con separador `,`.
5. No utilizar inferencia silenciosa de tipos para códigos con ceros a la izquierda.

### 14.2. Limpieza de SNIG

1. Normalizar nombres de columnas sin cambiar su significado.
2. Convertir `Anio` y `DepartamentoCodigo` a enteros.
3. Filtrar los cinco códigos departamentales.
4. En animales, filtrar `EspecieCodigo == 2`.
5. Convertir las variables de conteo a numéricas.
6. Convertir `UnidadesGanaderas` y `SuperficieGanadera`, que utilizan coma decimal.
7. Rechazar valores negativos en stocks, muertes, superficie o unidades ganaderas.
8. Agregar por departamento y año mediante suma.
9. Calcular los objetivos después de agregar.

### 14.3. Limpieza de INIA

1. Construir `Fecha` con año, mes y día.
2. Verificar que no haya fechas imposibles.
3. Verificar unicidad de `EstacionAgr + Fecha`.
4. Normalizar Unicode de los nombres de estación.
5. Aplicar el mapeo fijo estación–departamento.
6. Excluir Tacuarembó Glencore.
7. Convertir temperatura, precipitación y viento a numéricos.
8. Convertir viento de km/día a m/s.
9. Calcular CI diario.
10. Asignar `AnioEjercicio`.
11. Agregar las variables por departamento y ejercicio.

### 14.4. Integración

La unión final será:

```text
panel_SNIG
LEFT/INNER JOIN clima_INIA
ON DepartamentoCodigo + AnioEjercicio
```

Para el dataset modelable debe usarse una unión interna, después de comprobar y reportar qué registros quedarían fuera.

### 14.5. Controles de cardinalidad

Después de la integración se debe verificar:

```text
número de filas = 45
número de departamentos = 5
número de ejercicios = 9
duplicados DepartamentoCodigo + AnioEjercicio = 0
```

Para la versión con rezagos:

```text
número de filas = 40
número de ejercicios = 8
```

Si estas cantidades cambian, el pipeline debe detenerse y mostrar un error descriptivo.

---

## 15. Pseudocódigo de construcción del panel

```python
# 1. Cargar SNIG
animales = leer_csv_snig("DatosAnimales.csv")
generales = leer_csv_snig("DatosGenerales.csv")

# 2. Filtrar alcance
departamentos = [2, 4, 15, 18, 19]
ovinos = animales[
    animales["DepartamentoCodigo"].isin(departamentos)
    & (animales["EspecieCodigo"] == 2)
]

# 3. Agregar animales
animales_dep_anio = ovinos.groupby(
    ["DepartamentoCodigo", "Anio"], as_index=False
).agg(
    muertes_ovinas=("AnimalesPorEspecieMortandadPD_AD", "sum"),
    stock_ovino=("AnimalesPorEspeciePD_AD", "sum"),
    tenedores_ovinos=("CantidadTenedoresPorEspecie", "sum"),
)

animales_dep_anio["tasa_mortalidad_1000"] = (
    1000
    * animales_dep_anio["muertes_ovinas"]
    / animales_dep_anio["stock_ovino"]
)

# 4. Agregar datos generales
generales_dep_anio = generales.groupby(
    ["DepartamentoCodigo", "Anio"], as_index=False
).agg(
    unidades_ganaderas=("UnidadesGanaderas", "sum"),
    superficie_ganadera=("SuperficieGanadera", "sum"),
)

generales_dep_anio["intensidad_ug_ha"] = (
    generales_dep_anio["unidades_ganaderas"]
    / generales_dep_anio["superficie_ganadera"]
)

# 5. Preparar clima
inia["Fecha"] = construir_fecha(inia["Anio"], inia["Mes"], inia["Dia"])
inia["AnioEjercicio"] = donde(inia["Mes"] <= 6, inia["Anio"], inia["Anio"] + 1)
inia["viento_ms"] = inia["RecorridoViento"] / 86.4
inia["chill_index"] = calcular_chill_index(
    temperatura=inia["TempAireMedia"],
    viento_ms=inia["viento_ms"],
    precipitacion=inia["PrecipAcum"],
)

clima_dep_ejercicio = agregar_clima(inia)

# 6. Integrar
panel = (
    generales_dep_anio
    .merge(animales_dep_anio, on=["DepartamentoCodigo", "Anio"], validate="one_to_one")
    .merge(
        clima_dep_ejercicio,
        left_on=["DepartamentoCodigo", "Anio"],
        right_on=["DepartamentoCodigo", "AnioEjercicio"],
        validate="one_to_one",
    )
)

# 7. Filtrar ejercicios completos
panel = panel[panel["Anio"].between(2017, 2025)]

# 8. Crear rezagos por departamento
panel = panel.sort_values(["DepartamentoCodigo", "Anio"])
panel["intensidad_lag1"] = panel.groupby("DepartamentoCodigo")["intensidad_ug_ha"].shift(1)
panel["mortalidad_lag1"] = panel.groupby("DepartamentoCodigo")["tasa_mortalidad_1000"].shift(1)
```

El pseudocódigo es orientativo. La implementación deberá incluir validaciones, registro de errores y tests.

---

## 16. Prevención de fuga de información

Estas reglas son obligatorias:

1. No realizar una división aleatoria de filas.
2. Dejar años completos fuera durante la validación.
3. Ajustar escaladores únicamente con datos de entrenamiento.
4. Ajustar codificadores categóricos únicamente con entrenamiento.
5. Calcular el percentil de mortalidad elevada únicamente con entrenamiento.
6. Seleccionar hiperparámetros sin observar el año externo de prueba.
7. Crear rezagos antes de separar, pero usando únicamente valores cronológicamente anteriores dentro de cada departamento.
8. No usar mortalidad, nacimientos o stock del mismo ejercicio como predictor si no estarían disponibles antes del objetivo.
9. No tratar las filas originales de SNIG como observaciones climáticas independientes.
10. No usar los años 2022–2025 para imputar categorías MGAP faltantes de años anteriores.

Todo pipeline debe encapsular preprocesamiento y modelo para que el escalado no se ejecute sobre la tabla completa antes de la validación.

---

## 17. Diseño de modelos

### 17.1. Módulo de regresión

### Objetivo

Predecir `intensidad_ug_ha`.

### Baselines obligatorios

#### Baseline R1: promedio histórico del departamento

Para cada año de prueba, predecir el promedio de intensidad del departamento calculado solo con los años de entrenamiento.

#### Baseline R2: persistencia

Predecir la intensidad del ejercicio actual utilizando la intensidad del ejercicio anterior.

Este baseline es especialmente importante porque la intensidad cambia lentamente.

### Modelo principal

**Ridge Regression** con:

- variables climáticas estandarizadas;
- departamento codificado one-hot;
- opción con y sin rezago del objetivo; y
- penalización L2.

Ridge es el modelo principal porque:

- la muestra es pequeña;
- varias variables climáticas están correlacionadas;
- ofrece coeficientes interpretables; y
- reduce el riesgo de estimaciones extremas.

### Modelos secundarios

- regresión lineal simple como referencia;
- Elastic Net como análisis de sensibilidad; y
- árbol de regresión muy poco profundo como comparación no lineal.

No debe usarse un bosque aleatorio grande, XGBoost complejo o red neuronal como modelo principal. Con 40–45 observaciones, su flexibilidad puede generar sobreajuste sin evidencia de generalización.

### Grilla inicial de hiperparámetros

Ridge:

```text
alpha = [0.1, 1, 3, 10, 30, 100]
```

Elastic Net:

```text
alpha = [0.01, 0.1, 1, 10]
l1_ratio = [0.1, 0.5, 0.9]
```

Árbol:

```text
max_depth = [1, 2]
min_samples_leaf = [4, 6, 8]
```

La grilla no debe ampliarse después de observar el conjunto de prueba sin registrar una nueva ronda exploratoria.

### 17.2. Módulo de clasificación

### Objetivo

Predecir `MortalidadElevada`.

### Baselines obligatorios

#### Baseline C1: clase mayoritaria

Predecir siempre la clase más frecuente dentro del entrenamiento.

#### Baseline C2: persistencia de riesgo

Predecir que el ejercicio actual tendrá mortalidad elevada si el ejercicio anterior del mismo departamento fue elevado.

#### Baseline C3: historial departamental

Estimar una probabilidad constante igual a la proporción histórica de años elevados del departamento en entrenamiento.

### Modelo principal

**Regresión logística regularizada**, con:

- variables estandarizadas;
- departamento one-hot;
- `class_weight="balanced"` si existe desbalance relevante;
- regularización L2; y
- probabilidades calibradas únicamente si la cantidad de datos lo permite.

### Modelos secundarios

- regresión logística Elastic Net;
- árbol de clasificación con profundidad máxima 1 o 2; y
- bosque aleatorio muy restringido, solo como sensibilidad y nunca como única evidencia.

### Grilla inicial

Regresión logística:

```text
C = [0.01, 0.1, 0.3, 1, 3, 10]
penalty = "l2"
class_weight = [None, "balanced"]
```

Árbol:

```text
max_depth = [1, 2]
min_samples_leaf = [4, 6, 8]
class_weight = [None, "balanced"]
```

---

## 18. Protocolo de validación

### 18.1. Validación externa

Se utilizará **Leave-One-Year-Out**:

1. seleccionar un ejercicio como prueba;
2. usar todos los demás ejercicios como entrenamiento;
3. mantener juntos los cinco departamentos del ejercicio de prueba;
4. repetir para cada ejercicio; y
5. concatenar todas las predicciones fuera de muestra.

Para modelos sin rezago:

```text
9 folds: 2017, 2018, ..., 2025
5 observaciones de prueba por fold
45 predicciones fuera de muestra
```

Para modelos con rezago:

```text
8 folds: 2018, 2019, ..., 2025
5 observaciones de prueba por fold
40 predicciones fuera de muestra
```

### 18.2. Selección de hiperparámetros

Dentro de cada entrenamiento externo se utilizará una validación interna por año, también sin mezclar años.

Si el entrenamiento interno queda demasiado pequeño, se preferirá:

- fijar un hiperparámetro razonable antes de observar el fold externo; o
- utilizar una grilla mínima.

No se debe elegir el hiperparámetro que maximiza el resultado sobre las predicciones externas y luego presentar esa misma métrica como no sesgada.

### 18.3. Cálculo de métricas de clasificación

Cada año de prueba contiene solo cinco casos y puede no tener ambas clases. Por eso:

- no se debe promediar AUC por año si algún fold tiene una sola clase;
- se deben concatenar todas las probabilidades fuera de muestra;
- el AUC principal se calcula sobre las 40 o 45 predicciones concatenadas; y
- se reportan además resultados y errores por año.

### 18.4. Incertidumbre

Se reportará la variabilidad entre años y, como análisis descriptivo, intervalos obtenidos mediante bootstrap por bloques de año.

El bootstrap debe remuestrear años completos, no filas individuales.

Con solo nueve años, los intervalos serán amplios y deberán interpretarse como aproximaciones.

---

## 19. Métricas

### 19.1. Regresión

### Métrica primaria

**MAE — error absoluto medio**, expresado en UG/ha.

Se elige porque:

- mantiene la unidad del objetivo;
- es fácil de interpretar; y
- es menos sensible que RMSE a pocos errores extremos.

### Métricas secundarias

- RMSE;
- R² fuera de muestra;
- error porcentual solo cuando el denominador sea estable y no cercano a cero;
- MAE por departamento;
- MAE por ejercicio; y
- skill relativo frente a cada baseline.

Skill de MAE:

```text
Skill = 1 - MAE_modelo / MAE_baseline
```

Interpretación:

- `Skill > 0`: el modelo mejora al baseline;
- `Skill = 0`: empata;
- `Skill < 0`: es peor.

### 19.2. Clasificación

### Métrica primaria

**Balanced Accuracy** sobre predicciones fuera de muestra.

### Métricas secundarias

- ROC-AUC global;
- PR-AUC o Average Precision;
- F1 de la clase elevada;
- recall de mortalidad elevada;
- precisión de mortalidad elevada;
- especificidad;
- matriz de confusión; y
- Brier Score para probabilidades.

La accuracy simple no debe ser la única métrica porque puede verse favorecida por el desbalance de clases.

---

## 20. Criterios para considerar que existe valor predictivo

No alcanza con que el modelo tenga una métrica aparentemente buena. Para afirmar que las variables climáticas aportan valor deberán cumplirse, como mínimo, las siguientes condiciones:

1. El modelo debe superar tanto al baseline departamental como al de persistencia.
2. La mejora debe observarse en las predicciones fuera de muestra.
3. La mejora no debe depender de un único año extremo.
4. El signo y magnitud de los coeficientes climáticos deben ser razonablemente estables entre folds.
5. El desempeño debe ser consistente en varios departamentos.
6. El resultado debe mantenerse en al menos una especificación de sensibilidad.
7. No debe existir fuga temporal ni cálculo global del umbral de la clase.

Como regla práctica, una mejora inferior al 5 % en MAE frente al mejor baseline se considerará débil y no suficiente para una afirmación operacional.

Para clasificación, un AUC cercano a 0,50 o Balanced Accuracy cercana a 0,50 indicará ausencia de capacidad discriminativa útil.

---

## 21. Resultados preliminares de la auditoría

Estos resultados fueron obtenidos durante la evaluación de factibilidad y no sustituyen la implementación final reproducible:

### Regresión de intensidad

- Baseline de promedio histórico departamental: MAE aproximado de 0,026 UG/ha.
- Mejor Ridge climático más departamento en la prueba preliminar: MAE aproximado de 0,037 UG/ha.
- La referencia departamental fue mejor que el modelo climático.
- Al utilizar rezagos, la intensidad del año anterior fue más predictiva que agregar clima y uso del suelo.

### Clasificación de mortalidad elevada

- Modelo climático preliminar: Balanced Accuracy cercana a 0,50.
- ROC-AUC preliminar cercana a 0,49.
- El clima por sí solo no mostró discriminación fuera de muestra en esa prueba.
- La mortalidad previa presentó más capacidad predictiva que la combinación preliminar de clima y composición animal.

### Interpretación correcta

Los datos permiten ejecutar el proyecto y comparar modelos, pero actualmente no existe evidencia suficiente para prometer un predictor operacional. El trabajo debe evaluar rigurosamente si el clima aporta valor y aceptar como resultado válido que no lo aporte con la resolución disponible.

---

## 22. Análisis exploratorio obligatorio

El análisis exploratorio debe producir como mínimo:

1. tabla de cobertura por estación y año;
2. matriz de valores faltantes de las variables climáticas requeridas;
3. serie temporal de intensidad por departamento;
4. serie temporal de mortalidad por mil por departamento;
5. serie temporal de stock ovino y muertes por separado;
6. distribución de la tasa de mortalidad por departamento;
7. evolución anual de días por categoría de Chill Index;
8. relación entre precipitación anual y mortalidad;
9. relación entre días con CI >= 1000 y mortalidad;
10. relación entre días con CI >= 1200 y mortalidad;
11. correlaciones globales y correlaciones dentro de departamento;
12. identificación de años extremos;
13. comparación ejercicio completo frente a julio–octubre; y
14. gráfico de observados frente a predicciones fuera de muestra.

Todos los gráficos deben incluir:

- unidad;
- período;
- departamento cuando corresponda;
- fuente; y
- aclaración de si el valor es observado, agregado o predicho.

No se deben interpretar correlaciones globales sin controlar departamento, porque pueden reflejar diferencias estructurales entre regiones y no variación climática temporal.

---

## 23. Interpretabilidad

Para Ridge y regresión logística se reportarán:

- coeficientes estandarizados;
- signo del efecto;
- variación del coeficiente entre folds;
- importancia relativa frente al rezago; y
- predicciones por departamento y año.

La interpretación debe centrarse en estabilidad y desempeño fuera de muestra.

SHAP no será la herramienta principal porque:

- la muestra es muy pequeña;
- el modelo principal es lineal y ya tiene coeficientes interpretables; y
- una explicación detallada de un modelo que no supera baselines no aporta evidencia predictiva.

---

## 24. Estructura recomendada del repositorio

```text
JAI/
├── ESPECIFICACION_COMPLETA_PROYECTO.md
├── README.md
├── requirements.txt
├── config/
│   └── project.yaml
├── data/
│   ├── raw/
│   │   ├── INIA.csv
│   │   └── SNIG/
│   │       ├── DatosAnimales.csv
│   │       ├── DatosGenerales.csv
│   │       ├── Catalogos/
│   │       └── No usar/
│   ├── interim/
│   │   ├── clima_diario_con_ci.parquet
│   │   ├── clima_por_ejercicio.csv
│   │   ├── animales_por_departamento_anio.csv
│   │   └── generales_por_departamento_anio.csv
│   └── processed/
│       ├── panel_departamento_ejercicio.csv
│       └── diccionario_panel.md
├── notebooks/
│   ├── 01_auditoria_datos.ipynb
│   ├── 02_eda.ipynb
│   └── 03_revision_resultados.ipynb
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── load_snig.py
│   │   ├── load_inia.py
│   │   └── build_panel.py
│   ├── features/
│   │   ├── chill_index.py
│   │   └── build_features.py
│   ├── models/
│   │   ├── baselines.py
│   │   ├── regression.py
│   │   ├── classification.py
│   │   └── validation.py
│   └── reporting/
│       ├── figures.py
│       └── tables.py
├── tests/
│   ├── test_chill_index.py
│   ├── test_temporal_alignment.py
│   ├── test_aggregation.py
│   ├── test_panel.py
│   └── test_no_leakage.py
├── models/
│   └── final/
└── reports/
    ├── figures/
    ├── tables/
    └── informe_final.md
```

Los notebooks deben servir para exploración y comunicación. La lógica final debe migrarse a `src/` y probarse mediante `tests/`.

---

## 25. Configuración central

Se recomienda almacenar decisiones en `config/project.yaml`:

```yaml
project:
  random_seed: 42
  start_year: 2017
  end_year: 2025

departments:
  2:
    name: Canelones
    station: Las Brujas
  4:
    name: Colonia
    station: La Estanzuela
  15:
    name: Salto
    station: Salto Grande
  18:
    name: Tacuarembó
    station: Tacuarembó La Magnolia
  19:
    name: Treinta y Tres
    station: Treinta y Tres Paso de la Laguna

species:
  sheep_code: 2

climate:
  exercise_start_month: 7
  sensitive_months: [7, 8, 9, 10]
  minimum_coverage: 0.95
  wind_conversion_divisor: 86.4
  chill_thresholds: [900, 1000, 1100, 1200]

targets:
  mortality_per: 1000
  high_mortality_quantile: 0.75

validation:
  method: leave_one_year_out
```

Los nombres Unicode de las estaciones deben verificarse después de leer el archivo. Conviene normalizarlos mediante Unicode NFC antes de aplicar el mapeo.

---

## 26. Dependencias recomendadas

```text
Python >= 3.11
pandas
numpy
scikit-learn
matplotlib
seaborn
pyarrow
pyyaml
pytest
```

Opcionales:

```text
pandera        # validación de esquemas
statsmodels    # análisis estadístico complementario
joblib         # persistencia de modelos
```

Las versiones deben fijarse al iniciar la implementación para garantizar reproducibilidad.

---

## 27. Tests obligatorios

### 27.1. Tests de datos

- los años SNIG son 2016–2025;
- los códigos de departamento esperados existen;
- `EspecieCodigo == 2` corresponde a ovinos;
- no hay mortalidad negativa;
- no hay stock negativo;
- no hay superficie ganadera negativa;
- no hay duplicados departamento–ejercicio en el panel;
- existen 45 filas en el panel principal;
- existen 40 filas en el panel con rezagos; y
- ninguna fila modelable proviene de `No usar`.

### 27.2. Tests temporales

- 30 de junio pertenece al ejercicio del mismo año;
- 1 de julio pertenece al ejercicio siguiente;
- los rezagos respetan departamento;
- ningún rezago utiliza un año futuro; y
- no se incluye 2016 como ejercicio climático completo.

### 27.3. Tests del Chill Index

- conversión de viento;
- fórmula con valores conocidos;
- monotonicidad esperada;
- faltantes; y
- asignación de categorías en los límites 900, 1000, 1100 y 1200.

### 27.4. Tests contra fuga

- el escalador se ajusta dentro de cada fold;
- el percentil de la clase se calcula solo con entrenamiento;
- el año de prueba no participa en selección de hiperparámetros;
- la codificación del departamento se ajusta dentro del pipeline; y
- las predicciones reportadas son verdaderamente fuera de muestra.

---

## 28. Reproducibilidad

El proyecto debe registrar:

- versión de Python;
- versiones de dependencias;
- fecha de ejecución;
- hashes de los archivos raw;
- configuración utilizada;
- semilla aleatoria;
- lista exacta de variables;
- folds de validación;
- hiperparámetros seleccionados; y
- métricas fuera de muestra.

Los resultados generados no deben sobrescribirse silenciosamente. Cada ejecución relevante debe guardar un identificador o fecha.

La semilla recomendada es `42`, aunque los modelos lineales principales son deterministas.

---

## 29. Entregables

### Entregable 1: auditoría de datos

Debe contener:

- inventario de archivos;
- esquemas;
- períodos;
- nulos;
- duplicados;
- valores imposibles;
- cobertura climática; y
- decisiones de exclusión.

### Entregable 2: panel procesado

Archivo:

```text
data/processed/panel_departamento_ejercicio.csv
```

Debe contener una fila por departamento y ejercicio, componentes de los objetivos, objetivos calculados, variables climáticas, CI, cobertura y rezagos.

### Entregable 3: análisis exploratorio

Notebook y figuras con las visualizaciones obligatorias.

### Entregable 4: modelos y validación

- baselines;
- modelos de regresión;
- modelos de clasificación;
- predicciones fuera de muestra;
- métricas globales, por año y por departamento; y
- análisis de estabilidad.

### Entregable 5: informe final

Debe explicar:

- problema;
- fuentes;
- metodología;
- resultados;
- comparación con baselines;
- limitaciones;
- conclusiones; y
- posibles extensiones.

### Entregable 6: código y documentación

- código en `src/`;
- tests;
- `README.md` con instrucciones;
- configuración;
- dependencias; y
- este documento actualizado si cambia alguna decisión.

---

## 30. Plan de trabajo recomendado

### Fase 1: reproducir la auditoría

1. Crear entorno.
2. Fijar dependencias.
3. Implementar cargas.
4. Verificar esquemas.
5. Implementar tests básicos.

**Criterio de salida:** los resultados de cobertura, años, nulos y cantidades coinciden con esta especificación.

### Fase 2: construir el panel

1. Agregar SNIG.
2. Calcular objetivos.
3. Calcular CI diario.
4. Agregar clima por ejercicio.
5. Unir fuentes.
6. Crear rezagos.
7. Exportar panel y diccionario.

**Criterio de salida:** 45 filas sin duplicados y 40 filas en la versión rezagada.

### Fase 3: análisis exploratorio

1. Producir gráficos.
2. Examinar años extremos.
3. Comparar correlaciones globales y dentro de departamento.
4. Documentar decisiones sin seleccionar modelos por apariencia visual.

**Criterio de salida:** reporte EDA revisado por otra persona.

### Fase 4: baselines

1. Implementar baselines de regresión.
2. Implementar baselines de clasificación.
3. Generar predicciones fuera de muestra.

**Criterio de salida:** métricas reproducibles de referencia.

### Fase 5: modelos

1. Entrenar Ridge.
2. Entrenar regresión logística.
3. Ejecutar modelos secundarios limitados.
4. Comparar contra baselines.
5. Analizar estabilidad.

**Criterio de salida:** tabla única de resultados fuera de muestra.

### Fase 6: informe

1. Redactar resultados sin exageraciones.
2. Incluir limitaciones.
3. Revisar reproducibilidad.
4. Validar que cada cifra provenga de un artefacto guardado.

**Criterio de salida:** otra persona puede ejecutar el proyecto siguiendo el README.

---

## 31. Distribución sugerida de responsabilidades

Si el equipo tiene varias personas, se recomienda separar responsabilidades:

### Responsable de datos

- carga y limpieza;
- validación de esquemas;
- cálculo de CI;
- construcción del panel; y
- tests de datos.

### Responsable de modelado

- baselines;
- pipelines;
- validación temporal;
- selección de hiperparámetros; y
- métricas.

### Responsable de análisis

- EDA;
- visualizaciones;
- interpretación; y
- análisis por departamento.

### Responsable de documentación y revisión

- README;
- informe;
- control de referencias;
- revisión de afirmaciones; y
- verificación de reproducibilidad.

Aunque se distribuyan tareas, una segunda persona debe revisar el cálculo de objetivos, la alineación temporal y la ausencia de fuga.

---

## 32. Riesgos y mitigaciones

| Riesgo | Consecuencia | Mitigación |
|---|---|---|
| Solo 45 observaciones independientes | Alta varianza y sobreajuste | Modelos simples, pocas variables y validación temporal |
| Mortalidad anual sin fecha exacta | No permite atribuir muertes a episodios concretos | Trabajar con exposición anual y declarar la limitación |
| Mortalidad por especie, no por categoría | CI está más ligado a corderos que el objetivo disponible | Hablar de mortalidad ovina total y no neonatal |
| Denominador al cierre | La tasa no es incidencia exacta | Denominarla tasa proxy y analizar stock por separado |
| Una estación por departamento | Error de representación espacial | No extrapolar a establecimientos y discutir representatividad |
| Faltantes estructurales en clasificaciones MGAP | Riesgo de codificar el período | Excluir esas columnas |
| Alta correlación entre variables CI | Coeficientes inestables | Ridge y conjuntos reducidos de variables |
| Intensidad muy persistente | Clima puede no superar el último valor | Incluir baseline de persistencia |
| Clase elevada pequeña | Métricas inestables | Balanced Accuracy, PR-AUC y pesos de clase |
| Selección excesiva de modelos | Optimismo por múltiples pruebas | Predefinir modelos y grillas |
| Confundir asociación con causalidad | Conclusiones incorrectas | Usar lenguaje predictivo y observacional |

---

## 33. Afirmaciones permitidas y no permitidas

### Se puede afirmar, si los resultados lo respaldan

- “El Chill Index presenta asociación con la mortalidad ovina anual agregada.”
- “El modelo mejora o no mejora al baseline en validación fuera de muestra.”
- “La capacidad predictiva difiere entre departamentos.”
- “Las variables climáticas aportan una mejora de X % en MAE respecto del baseline.”
- “El modelo identifica años de mortalidad elevada con determinada sensibilidad y especificidad.”

### No se puede afirmar con estos datos

- “El Chill Index causó las muertes observadas.”
- “El modelo predice la muerte de un animal individual.”
- “El modelo predice específicamente muertes de corderos.”
- “El modelo funciona para todo Uruguay.”
- “Cada fila original de SNIG es una observación independiente.”
- “Una accuracy alta demuestra utilidad si existe desbalance.”
- “El CI superior a 1200 equivale automáticamente a mortalidad anual elevada.”
- “El sistema constituye una alerta operacional en tiempo real.”

---

## 34. Criterios de aceptación del proyecto

El proyecto se considerará correctamente ejecutado si:

- [ ] los archivos raw permanecen sin modificaciones;
- [ ] el CI se calcula con unidades correctas;
- [ ] el ejercicio se alinea julio–junio;
- [ ] el panel principal tiene 45 filas únicas;
- [ ] el panel rezagado tiene 40 filas únicas;
- [ ] se documentan faltantes y cobertura;
- [ ] las dos columnas MGAP incompletas quedan excluidas;
- [ ] los objetivos se calculan a partir de totales agregados;
- [ ] se implementan baselines;
- [ ] la validación deja años completos fuera;
- [ ] el umbral de clasificación se calcula dentro de cada entrenamiento;
- [ ] todas las métricas principales son fuera de muestra;
- [ ] se reportan resultados negativos si el modelo no supera baselines;
- [ ] las conclusiones respetan las limitaciones; y
- [ ] otra persona puede reproducir el flujo completo.

---

## 35. Decisiones metodológicas cerradas

Para evitar que distintos integrantes implementen versiones incompatibles, se consideran cerradas las siguientes decisiones:

1. La unidad es departamento–ejercicio.
2. El ejercicio va de julio a junio.
3. El período principal es 2017–2025.
4. La especie analizada es ovinos, código 2.
5. Se utilizan cinco departamentos.
6. Tacuarembó se representa con La Magnolia.
7. El viento se convierte de km/día a m/s dividiendo por 86,4.
8. El CI se calcula con la fórmula oficial de INIA.
9. La intensidad es UG dividida entre superficie ganadera agregada.
10. La mortalidad se expresa como una tasa proxy por mil.
11. La clase elevada usa el percentil 75 departamental calculado en entrenamiento.
12. Los umbrales CI no construyen la etiqueta de mortalidad.
13. Las clasificaciones MGAP incompletas se excluyen.
14. El modelo principal de regresión es Ridge.
15. El modelo principal de clasificación es regresión logística regularizada.
16. La validación es Leave-One-Year-Out.
17. Los baselines son obligatorios.
18. No se construye dashboard.
19. No se presenta el resultado como causal.
20. No se promete una herramienta operacional si no se superan baselines.

Cualquier cambio en estas decisiones debe registrarse en una sección de historial, explicar su motivo y actualizar código, tests y documentación.

---

## 36. Posibles extensiones futuras

Estas extensiones no forman parte de la primera versión:

1. incorporar datos climáticos espaciales en grilla para obtener variación dentro de cada departamento;
2. incorporar una serie histórica anterior a 2016;
3. obtener mortalidad mensual o fechada;
4. separar mortalidad de corderos y adultos;
5. incorporar fechas de parición y esquila;
6. modelar conteos con una distribución Poisson o binomial negativa y usar stock como exposición;
7. incorporar información forrajera o hídrica espacial;
8. realizar validación externa en departamentos adicionales; y
9. convertir el modelo validado en una herramienta operacional con pronósticos meteorológicos.

Estas extensiones solo deben considerarse después de completar la versión básica y demostrar que el problema, el objetivo y la validación están correctamente definidos.

---

## 37. Glosario

**AUC:** área bajo la curva ROC. Mide capacidad de ordenamiento entre clases.  
**Baseline:** método simple utilizado como referencia mínima.  
**Chill Index:** índice de pérdida potencial de calor asociado a temperatura, viento y precipitación.  
**DICOSE:** sistema de declaraciones ganaderas administrado por MGAP/SNIG.  
**Ejercicio ganadero:** período del 1 de julio al 30 de junio siguiente.  
**Fuga de información:** uso durante entrenamiento de datos que no estarían disponibles al predecir.  
**INIA:** Instituto Nacional de Investigación Agropecuaria.  
**Intensidad ganadera:** unidades ganaderas por hectárea ganadera.  
**MAE:** promedio del valor absoluto de los errores.  
**MGAP:** Ministerio de Ganadería, Agricultura y Pesca.  
**Mortalidad elevada:** tasa proxy superior al percentil 75 histórico departamental del conjunto de entrenamiento.  
**PD_AD:** sufijo utilizado por SNIG en las variables elegidas de mortalidad y existencia; se mantiene el mismo universo en numerador y denominador.  
**Persistencia:** baseline que usa el último valor conocido como predicción.  
**Pseudorreplicación:** tratar registros que comparten la misma exposición como observaciones independientes.  
**Ridge:** regresión lineal con penalización L2.  
**SNIG:** Sistema Nacional de Información Ganadera.  
**Tasa proxy:** indicador aproximado que no cumple todos los requisitos de una tasa de incidencia exacta.  
**UG:** unidad ganadera.  

---

## 38. Referencias principales

1. INIA. “Previsión para Corderos” y metodología del Chill Index.  
   <https://inia.uy/gras/Aplicaciones_y_recursos/Prevision%20Corderos>

2. INIA GRAS. Banco de datos agroclimáticos y listado de variables.  
   <https://gras.inia.uy/gras/es/ConsultasWebDBC/consulta_bdagroclima/>

3. MGAP. Presentación de Declaración Jurada Anual de DICOSE.  
   <https://www.gub.uy/tramites/presentacion-declaracion-jurada-dicose>

4. Catálogo Nacional de Datos Abiertos. Declaración jurada de existencias DICOSE–SNIG.  
   <https://catalogodatos.gub.uy/es/dataset/mgap-datos-preliminares-basados-en-la-declaracion-jurada-de-existencias-dicose-snig-2024>

5. Nixon-Smith, W. F. (1972). *The forecasting of chill risk ratings for newborn lambs and off-shears sheep by use of a cooling factor derived from synoptic data*. Bureau of Meteorology, Canberra, Working Paper No. 150.

6. Donnelly, J. R. (1984). “The productivity of breeding ewes grazing on lucerne or grass and clover pastures on the tablelands of southern Australia”. *Australian Journal of Agricultural Research*, 35, 709–721.

---

## 39. Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-10-28 | Primera especificación completa basada en la auditoría de SNIG e INIA |

