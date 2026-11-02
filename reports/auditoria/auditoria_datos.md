# Auditoría de datos crudos

Generado: 2026-10-30T10:29:53 · Python 3.12.7 · pandas 3.1.0 · numpy 2.5.4

Archivo generado por `python -m src.data.audit`. No editar a mano.

## Verificación de la sección 9

22 de 22 chequeos correctos.

| chequeo | esperado | observado | ok |
|---|---|---|---|
| Filas DatosAnimales | 677035 | 677035 | True |
| Filas DatosGenerales | 315536 | 315536 | True |
| Años DatosAnimales | 2016–2025 | 2016–2025 | True |
| Años DatosGenerales | 2016–2025 | 2016–2025 | True |
| Filas ovinas en los 5 departamentos | 40418 | 40418 | True |
| Combinaciones departamento–año (ovinos) | 50 | 50 | True |
| Combinaciones departamento–año (generales) | 50 | 50 | True |
| Departamento–ejercicio 2017–2025 con cobertura climática mínima | 45 | 45 | True |
| Duplicados clave dimensional completa (DatosAnimales) | 0 | 0 | True |
| Duplicados clave dimensional completa (DatosGenerales) | 0 | 0 | True |
| Mortalidad ovina nula | 0 | 0 | True |
| Mortalidad ovina negativa | 0 | 0 | True |
| Ovinos modelables 2017–2025 completos y no negativos | sin errores | sin errores | True |
| DatosGenerales modelable 2017–2025 completo y no negativo | sin errores | sin errores | True |
| Columnas MGAP 100 % nulas en 2016–2021 | True | True | True |
| Columnas MGAP completas desde 2022 | True | True | True |
| Cobertura mínima de las estaciones seleccionadas en 2017–2025 | >= 0.95 | 0.9945 | True |
| Ejercicios con cobertura suficiente en estaciones excluidas | < 9 | 0 | True |
| Duplicados estación–fecha en INIA | 0 | 0 | True |
| Primera fecha INIA | 2016-01-01 | 2016-01-01 | True |
| Última fecha INIA | 2026-03-17 | 2026-03-17 | True |
| Archivos raw sin modificaciones (SHA-256) | True | True | True |

## Inventario

| archivo | bytes | filas |
|---|---|---|
| data/raw/Departamentos.csv | 267 |  |
| data/raw/EstacionAgr.csv | 168 |  |
| data/raw/INIA.csv | 4887777 | 21402 |
| data/raw/Metadatos INIA.txt | 11380 |  |
| data/raw/SNIG/Catalogos/Departamentos.csv | 267 |  |
| data/raw/SNIG/Catalogos/Especies.csv | 116 |  |
| data/raw/SNIG/DatosAnimales.csv | 38569867 | 677035 |
| data/raw/SNIG/DatosGenerales.csv | 18261195 | 315536 |

## Columnas MGAP: % de nulos por año

| Anio | DatosAnimales.EspecializacionMGAPCodigo_nulos_pct | DatosAnimales.TipoProduccionMGAPCodigo_nulos_pct | DatosGenerales.EspecializacionMGAPCodigo_nulos_pct | DatosGenerales.TipoProduccionMGAPCodigo_nulos_pct |
|---|---|---|---|---|
| 2016 | 100.0 | 100.0 | 100.0 | 100.0 |
| 2017 | 100.0 | 100.0 | 100.0 | 100.0 |
| 2018 | 100.0 | 100.0 | 100.0 | 100.0 |
| 2019 | 100.0 | 100.0 | 100.0 | 100.0 |
| 2020 | 100.0 | 100.0 | 100.0 | 100.0 |
| 2021 | 100.0 | 100.0 | 100.0 | 100.0 |
| 2022 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2023 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2024 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2025 | 0.0 | 0.0 | 0.0 | 0.0 |

## Duplicados

| archivo | clave | duplicados |
|---|---|---|
| DatosAnimales | dimensiones + MGAP | 0 |
| DatosAnimales | dimensiones sin MGAP | 74185 |
| DatosAnimales | fila completa sin ID | 0 |
| DatosGenerales | dimensiones + MGAP | 0 |
| DatosGenerales | dimensiones sin MGAP | 43018 |
| DatosGenerales | fila completa sin ID | 0 |
| INIA | estación + fecha | 0 |

## Valores imposibles

| archivo | columna | regla | violaciones |
|---|---|---|---|
| DatosAnimales | AnimalesPorEspecieConsumoPD_AD | >= 0 | 1 |
| DatosAnimales | AnimalesPorEspecieNacimientosPD_AD | >= 0 | 0 |
| DatosAnimales | AnimalesPorEspecieMortandadPD_AD | >= 0 | 0 |
| DatosAnimales | CantidadTenedoresPorEspecie | >= 0 | 0 |
| DatosAnimales | AnimalesPorEspeciePD_AD | >= 0 | 0 |
| DatosAnimales | AnimalesPorEspeciePD_PF | >= 0 | 0 |
| DatosGenerales | Superficie | >= 0 | 0 |
| DatosGenerales | CantidadTenedores | >= 0 | 0 |
| DatosGenerales | UnidadesGanaderas | >= 0 | 0 |
| DatosGenerales | SuperficieGanadera | >= 0 | 4 |
| INIA | TempAireMedia | entre -15 y 45 | 0 |
| INIA | PrecipAcum | entre 0 y 500 | 0 |
| INIA | RecorridoViento | entre 0 y 2000 | 0 |

## Faltantes climáticos por estación

| EstacionAgr | dias | primera_fecha | ultima_fecha | TempAireMedia_faltantes | PrecipAcum_faltantes | RecorridoViento_faltantes |
|---|---|---|---|---|---|---|
| La Estanzuela | 3729 | 2016-01-01 | 2026-03-17 | 0 | 0 | 2 |
| Las Brujas | 3728 | 2016-01-01 | 2026-03-16 | 0 | 0 | 2 |
| Salto Grande | 3729 | 2016-01-01 | 2026-03-17 | 0 | 0 | 1 |
| Tacuarembó La Magnolia | 3729 | 2016-01-01 | 2026-03-17 | 0 | 0 | 2 |
| Tacuaremnó Glencore | 2765 | 2016-11-01 | 2026-03-17 | 0 | 2 | 904 |
| Treinta y Tres Paso de la Laguna | 3722 | 2016-01-01 | 2026-03-10 | 0 | 1 | 10 |

## Cobertura climática por estación y ejercicio (%)

Días con temperatura, precipitación y viento sobre los días del ejercicio julio–junio. Los ejercicios 2016 y 2026 son parciales por el rango del archivo.

| EstacionAgr | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| La Estanzuela | 49.7 | 100.0 | 100.0 | 99.7 | 100.0 | 100.0 | 100.0 | 100.0 | 99.7 | 100.0 | 71.2 |
| Las Brujas | 49.7 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.4 | 100.0 | 100.0 | 100.0 | 71.0 |
| Salto Grande | 49.7 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 71.0 |
| Tacuarembó La Magnolia | 49.7 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.7 | 100.0 | 100.0 | 100.0 | 71.0 |
| Tacuaremnó Glencore | 0.0 | 65.2 | 91.0 | 0.0 | 0.0 | 0.0 | 92.0 | 94.5 | 88.5 | 63.0 | 15.1 |
| Treinta y Tres Paso de la Laguna | 49.4 | 99.7 | 100.0 | 99.7 | 99.4 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 67.7 |

## Decisiones de exclusión

- Estación **Tacuaremnó Glencore** excluida: comienza el 2016-11-01 y le falta 32.7 % de `RecorridoViento`.
- Columnas `EspecializacionMGAPCodigo`, `TipoProduccionMGAPCodigo` excluidas: vacías en 2016–2021, no se imputan.
- 1 fila(s) de DatosAnimales con `DepartamentoCodigo` fuera del catálogo (códigos [0]); quedan fuera por el filtro de departamentos.
- 2 fila(s) de DatosGenerales con `UnidadesGanaderas` o `SuperficieGanadera` enmascarada como `********` (departamento, año: [(17, 2018)]). Se cargan como faltantes; el pipeline se detiene si alguna cae dentro del alcance modelable.
- 4 fila(s) de DatosGenerales con `UnidadesGanaderas` o `SuperficieGanadera` negativa (departamento, año: [(2, 2016), (4, 2016), (14, 2016), (16, 2016)]). Ninguna está en el período 2017–2025; el pipeline se detiene si aparece alguna.
- Ejercicio 2016 excluido como observación principal: requiere clima desde julio del año anterior y INIA comienza en enero.
- Temperatura: se usa `TempAireMedia`. `TMedia` difiere en promedio 0.19 °C y no se utiliza.
- Los nombres de estación de INIA mezclan Unicode NFC y NFD; se normalizan a NFC antes del mapeo.

Los esquemas completos por columna están en los CSV `esquema_*.csv` de esta carpeta.
