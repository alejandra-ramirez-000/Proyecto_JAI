# Proyecto JAI — Chill Index, intensidad ganadera y mortalidad ovina

Evaluación de la capacidad predictiva del Chill Index y otras variables agroclimáticas (INIA) sobre la intensidad ganadera y la mortalidad ovina anual (SNIG/DICOSE) en Canelones, Colonia, Salto, Tacuarembó y Treinta y Tres, ejercicios ganaderos 2017–2025.

La metodología completa y las decisiones cerradas están en [ESPECIFICACION_COMPLETA_PROYECTO.md](ESPECIFICACION_COMPLETA_PROYECTO.md).

## Requisitos

- Python >= 3.11 (probado con 3.12.7)

## Instalación

```bash
python -m venv .venv
```

Activar el entorno (Windows / Git Bash: `source .venv/Scripts/activate`; PowerShell: `.venv\Scripts\Activate.ps1`; Linux/macOS: `source .venv/bin/activate`) e instalar:

```bash
pip install -r requirements.txt
```

Para reproducir el entorno exacto, incluidas dependencias transitivas, usar `requirements-lock.txt`.

## Tests

```bash
python -m pytest
```

## Auditoría de datos (Fase 1)

```bash
python -m src.data.audit
```

Verifica los hallazgos de la sección 9 de la especificación y genera `reports/auditoria/` (resumen en `auditoria_datos.md` y tablas CSV). Termina con error si algún chequeo no coincide.

Los SHA-256 de `data/raw/` están registrados en `config/raw_sha256.txt`, y un test verifica que los archivos no cambien. Solo si se reemplazan los datos crudos a propósito:

```bash
python -m src.data.audit --registrar-hashes
```

## Panel departamento–ejercicio (Fase 2)

```bash
python -m src.data.build_panel
```

Calcula el Chill Index diario, agrega clima (ejercicio completo y julio–octubre) y SNIG por departamento y ejercicio, crea los rezagos y escribe:

- `data/interim/`: clima diario con CI (parquet) y agregados intermedios.
- `data/processed/panel_departamento_ejercicio.csv`: 45 filas (40 con rezagos).
- `data/processed/diccionario_panel.md`: descripción, unidad y rol de cada columna.
- `data/processed/panel_metadata.json`: fecha, versiones, hashes raw y configuración de la ejecución.

Se detiene con error si la cardinalidad o la cobertura climática no son las esperadas.

## Análisis exploratorio (Fase 3)

```bash
python -m src.reporting.eda
```

Requiere haber corrido `src.data.build_panel`. Genera las figuras obligatorias de la sección 22 en `reports/figures/`, las tablas en `reports/tables/` y el resumen `reports/eda.md`. La interpretación escrita está en `reports/eda_observaciones.md`, que se edita a mano y hay que revisar si cambian las cifras.

## Validación y baselines (Fase 4)

```bash
python -m src.models.baselines
```

Evalúa con Leave-One-Year-Out los baselines obligatorios: R1 promedio departamental y R2 persistencia para intensidad; C1 clase mayoritaria, C2 persistencia de riesgo y C3 historial departamental para mortalidad elevada. Lo hace en dos conjuntos: `completo` (45 filas, 9 folds) y `con_rezago` (40 filas, 8 folds). La etiqueta de mortalidad elevada (percentil 75 departamental) se recalcula dentro de cada fold.

Cada corrida se guarda en una carpeta nueva `reports/runs/<fecha-hora>_<nombre>/` y nunca sobrescribe una anterior. Contiene:

- predicciones fuera de muestra;
- métricas globales con IC 95 % por bootstrap de ejercicios completos;
- métricas por departamento y por año;
- skill frente a cada baseline;
- `resumen.md` y `metadata.json` (versiones, semilla, hashes, folds, configuración).

La lógica común está en `src/models/validation.py` y `src/models/experiment.py`, y la reutilizan los modelos de la Fase 5.

## Modelos (Fase 5)

```bash
python -m src.models.run_models
```

Corre en una misma corrida los baselines y los modelos.

- **Conjuntos de variables** (`src/models/feature_sets.py`):
  - A: clima básico;
  - B: exposición al Chill Index;
  - C-A y C-B: A o B más el rezago del objetivo;
  - H: control con solo el rezago, sin clima.

  Cada conjunto se corre en las ventanas ejercicio completo y julio–octubre.
- **Regresión** (`src/models/regression.py`): Ridge como modelo principal; regresión lineal, Elastic Net y árbol como secundarios.
- **Clasificación** (`src/models/classification.py`): logística L2 como modelo principal; logística Elastic Net y árbol como secundarios; bosque restringido solo como sensibilidad.

Los hiperparámetros se eligen con validación interna por año dentro de cada fold (`src/models/tuning.py`). El escalado y el one-hot del departamento se ajustan dentro del pipeline.

La corrida agrega a lo de la Fase 4:

- hiperparámetros y coeficientes por fold;
- la tabla de criterios de la sección 20 (`criterios_*.csv`, `src/models/assessment.py`);
- la figura 14 del EDA (observados frente a predichos), que también se copia a `reports/figures/`.

**Ronda exploratoria registrada.** Corre Ridge y logística con hiperparámetros fijos:

```bash
python -m src.models.run_exploratory
```

Se definió después de ver la corrida principal para diagnosticar la selección de hiperparámetros, así que no reemplaza a sus resultados. Su `resumen.md` y su `metadata.json` lo indican explícitamente.

## Informe final (Fase 6)

El informe está en [reports/informe_final.md](reports/informe_final.md). Sus cifras se generan desde los artefactos guardados con:

```bash
python -m src.reporting.informe_cifras
```

El comando escribe `reports/tables/informe_cifras.csv`, con la fuente de cada cifra. `tests/test_informe.py` verifica que se regeneran idénticas, que existen las corridas citadas y que existen las imágenes enlazadas.

## Reproducir todo desde cero

```bash
python -m src.data.audit
python -m src.data.build_panel
python -m src.reporting.eda
python -m src.models.run_models
python -m src.models.run_exploratory
python -m src.reporting.informe_cifras
python -m pytest
```

Para tener en cuenta:

- `run_models` y `run_exploratory` crean carpetas nuevas en `reports/runs/` con la fecha y hora de la corrida. El informe cita las corridas de referencia por nombre, en `src/reporting/informe_cifras.py`.
- Los resultados son deterministas: todo estimador aleatorio tiene semilla fija.

## Estructura

```text
config/project.yaml   decisiones centrales (departamentos, estaciones, umbrales, años)
data/raw/             datos originales, inmutables — no editar
data/interim/         artefactos intermedios regenerables (no versionados)
data/processed/       panel departamento–ejercicio final
notebooks/            exploración y comunicación
src/                  lógica del pipeline (data, features, models, reporting)
tests/                tests de datos, temporales, Chill Index y fuga de información
models/final/         modelos serializados (no versionados)
reports/              figuras, tablas e informe final
```

## Estado

| Fase | Descripción | Estado |
|---|---|---|
| 0 | Preparación del repositorio y entorno | Hecha |
| 1 | Carga y auditoría de datos | Hecha |
| 2 | Chill Index y panel | Hecha |
| 3 | Análisis exploratorio | Hecha (falta revisión por otra persona) |
| 4 | Validación y baselines | Hecha |
| 5 | Modelos | Hecha (falta revisión; ver `reports/modelos_observaciones.md`) |
| 6 | Informe y reproducibilidad | Hecha (falta revisión por otra persona) |
