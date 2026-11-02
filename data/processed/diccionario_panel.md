# Diccionario del panel departamento–ejercicio

Archivo: `data/processed/panel_departamento_ejercicio.csv`. Generado por `python -m src.data.build_panel`; no editar a mano.

- Una fila por `DepartamentoCodigo` + `AnioEjercicio`: 45 filas, ejercicios 2017–2025.
- Los rezagos son faltantes en el primer ejercicio de cada departamento; el panel con rezagos tiene 40 filas.
- Las variables climáticas se calculan sobre días válidos; los días incompletos no se imputan.
- Fuentes: SNIG/DICOSE (DatosAnimales, DatosGenerales) e INIA (banco de datos agroclimáticos).

| columna | descripción | unidad | rol |
|---|---|---|---|
| `DepartamentoCodigo` | Código SNIG del departamento (categórico, no continuo) | - | identificación |
| `Departamento` | Nombre del departamento | - | identificación |
| `AnioEjercicio` | Ejercicio ganadero: 1 de julio del año anterior al 30 de junio | año | identificación |
| `EstacionAgr` | Estación INIA asignada al departamento | - | identificación |
| `unidades_ganaderas` | Suma de UnidadesGanaderas (DatosGenerales) | UG | componente del objetivo |
| `superficie_ganadera` | Suma de SuperficieGanadera (DatosGenerales) | ha | componente del objetivo |
| `superficie_total` | Suma de Superficie (DatosGenerales) | ha | descriptiva — no usar como predictor |
| `tenedores_total` | Suma de CantidadTenedores (DatosGenerales) | tenedores | descriptiva — no usar como predictor |
| `intensidad_ug_ha` | unidades_ganaderas / superficie_ganadera | UG/ha | objetivo (regresión) |
| `muertes_ovinas` | Suma de AnimalesPorEspecieMortandadPD_AD, ovinos | animales | componente del objetivo |
| `stock_ovino` | Suma de AnimalesPorEspeciePD_AD, ovinos (existencia declarada al cierre) | animales | componente del objetivo |
| `tenedores_ovinos` | Suma de CantidadTenedoresPorEspecie, ovinos | tenedores | descriptiva — no usar como predictor |
| `nacimientos_ovinos` | Suma de AnimalesPorEspecieNacimientosPD_AD, ovinos (simultáneo al objetivo) | animales | descriptiva — no usar como predictor |
| `stock_ovino_pd_pf` | Suma de AnimalesPorEspeciePD_PF, ovinos; solo para sensibilidad del denominador | animales | descriptiva — no usar como predictor |
| `tasa_mortalidad_1000` | Tasa proxy de mortalidad ovina: 1000 × muertes_ovinas / stock_ovino. La etiqueta de mortalidad elevada NO está en el panel: se calcula dentro de cada fold | muertes por mil | objetivo (continuo y base de la clasificación) |
| `dias_esperados_ejercicio` | Días calendario de la ventana; ejercicio completo (jul–jun) | días | control de calidad |
| `dias_validos_ejercicio` | Días con temperatura, precipitación y viento (CI calculable); ejercicio completo (jul–jun) | días | control de calidad |
| `cobertura_ejercicio` | dias_validos / dias_esperados (mínimo exigido 0,95); ejercicio completo (jul–jun) | proporción | control de calidad |
| `temp_media_c_ejercicio` | Promedio de TempAireMedia en días válidos; ejercicio completo (jul–jun) | °C | predictor climático |
| `precip_total_mm_ejercicio` | Suma de PrecipAcum en días válidos; ejercicio completo (jul–jun) | mm | predictor climático |
| `viento_medio_ms_ejercicio` | Promedio de RecorridoViento / 86,4 en días válidos; ejercicio completo (jul–jun) | m/s | predictor climático |
| `ci_medio_ejercicio` | Promedio del Chill Index diario; ejercicio completo (jul–jun) | kJ/m²/h | predictor climático |
| `ci_max_ejercicio` | Máximo del Chill Index diario; ejercicio completo (jul–jun) | kJ/m²/h | predictor climático |
| `ci_p95_ejercicio` | Percentil 95 del Chill Index diario; ejercicio completo (jul–jun) | kJ/m²/h | predictor climático |
| `dias_ci_ge_900_ejercicio` | Días con CI >= 900; ejercicio completo (jul–jun) | días | predictor climático |
| `dias_ci_ge_1000_ejercicio` | Días con CI >= 1000; ejercicio completo (jul–jun) | días | predictor climático |
| `dias_ci_ge_1100_ejercicio` | Días con CI >= 1100; ejercicio completo (jul–jun) | días | predictor climático |
| `dias_ci_ge_1200_ejercicio` | Días con CI >= 1200; ejercicio completo (jul–jun) | días | predictor climático |
| `prop_ci_ge_1000_ejercicio` | Proporción de días válidos con CI >= 1000; ejercicio completo (jul–jun) | proporción | predictor climático |
| `racha_max_ci_ge_1000_ejercicio` | Máxima cantidad de días consecutivos con CI >= 1000; ejercicio completo (jul–jun) | días | predictor climático |
| `prop_ci_ge_1200_ejercicio` | Proporción de días válidos con CI >= 1200; ejercicio completo (jul–jun) | proporción | predictor climático |
| `racha_max_ci_ge_1200_ejercicio` | Máxima cantidad de días consecutivos con CI >= 1200; ejercicio completo (jul–jun) | días | predictor climático |
| `dias_esperados_jul_oct` | Días calendario de la ventana; julio–octubre | días | control de calidad |
| `dias_validos_jul_oct` | Días con temperatura, precipitación y viento (CI calculable); julio–octubre | días | control de calidad |
| `cobertura_jul_oct` | dias_validos / dias_esperados (mínimo exigido 0,95); julio–octubre | proporción | control de calidad |
| `temp_media_c_jul_oct` | Promedio de TempAireMedia en días válidos; julio–octubre | °C | predictor climático |
| `precip_total_mm_jul_oct` | Suma de PrecipAcum en días válidos; julio–octubre | mm | predictor climático |
| `viento_medio_ms_jul_oct` | Promedio de RecorridoViento / 86,4 en días válidos; julio–octubre | m/s | predictor climático |
| `ci_medio_jul_oct` | Promedio del Chill Index diario; julio–octubre | kJ/m²/h | predictor climático |
| `ci_max_jul_oct` | Máximo del Chill Index diario; julio–octubre | kJ/m²/h | predictor climático |
| `ci_p95_jul_oct` | Percentil 95 del Chill Index diario; julio–octubre | kJ/m²/h | predictor climático |
| `dias_ci_ge_900_jul_oct` | Días con CI >= 900; julio–octubre | días | predictor climático |
| `dias_ci_ge_1000_jul_oct` | Días con CI >= 1000; julio–octubre | días | predictor climático |
| `dias_ci_ge_1100_jul_oct` | Días con CI >= 1100; julio–octubre | días | predictor climático |
| `dias_ci_ge_1200_jul_oct` | Días con CI >= 1200; julio–octubre | días | predictor climático |
| `prop_ci_ge_1000_jul_oct` | Proporción de días válidos con CI >= 1000; julio–octubre | proporción | predictor climático |
| `racha_max_ci_ge_1000_jul_oct` | Máxima cantidad de días consecutivos con CI >= 1000; julio–octubre | días | predictor climático |
| `prop_ci_ge_1200_jul_oct` | Proporción de días válidos con CI >= 1200; julio–octubre | proporción | predictor climático |
| `racha_max_ci_ge_1200_jul_oct` | Máxima cantidad de días consecutivos con CI >= 1200; julio–octubre | días | predictor climático |
| `intensidad_lag1` | intensidad_ug_ha del ejercicio anterior, mismo departamento | UG/ha | predictor histórico (rezago) |
| `mortalidad_lag1` | tasa_mortalidad_1000 del ejercicio anterior, mismo departamento | muertes por mil | predictor histórico (rezago) |
| `stock_ovino_lag1` | stock_ovino del ejercicio anterior, mismo departamento | animales | predictor histórico (rezago) |
| `tenedores_ovinos_lag1` | tenedores_ovinos del ejercicio anterior, mismo departamento | tenedores | predictor histórico (rezago) |
