"""Conjuntos de variables predefinidos (sección 13.6).

Están fijados antes de ver resultados de modelos. El departamento entra
siempre como categórico (one-hot) dentro del pipeline, nunca como número.

- A: clima básico.
- B: exposición al Chill Index.
- C-A / C-B: el conjunto A o B más el rezago del objetivo.
- H: control sin clima (solo rezago y departamento). No figura en la
  sección 13.6; se agrega como control, definido antes de correr los modelos,
  para medir si el clima aporta por encima de la historia propia
  (pregunta principal, sección 2).
"""

from src.features.build_features import FULL_WINDOW, SENSITIVE_WINDOW

DEPT = "DepartamentoCodigo"
WINDOWS = (FULL_WINDOW, SENSITIVE_WINDOW)

CLIMATE_SETS = {
    "A": ["temp_media_c", "precip_total_mm", "viento_medio_ms"],
    "B": ["dias_ci_ge_1000", "dias_ci_ge_1200", "ci_max"],
}

TARGET_LAGS = {
    "intensidad_ug_ha": "intensidad_lag1",
    "tasa_mortalidad_1000": "mortalidad_lag1",
}


def climate_columns(set_name: str, window: str) -> list[str]:
    return [f"{v}_{window}" for v in CLIMATE_SETS[set_name]]


def feature_specs(target: str) -> list[dict]:
    """Todas las especificaciones para un objetivo: nombre, columnas numéricas, ventana y si usa rezago."""
    lag = TARGET_LAGS[target]
    specs = []
    for window in WINDOWS:
        for set_name in CLIMATE_SETS:
            cols = climate_columns(set_name, window)
            specs.append({"set": set_name, "window": window, "numeric": cols, "requires_lag": False})
            specs.append({"set": f"C-{set_name}", "window": window, "numeric": cols + [lag], "requires_lag": True})
    specs.append({"set": "H", "window": "sin_clima", "numeric": [lag], "requires_lag": True})
    return specs
