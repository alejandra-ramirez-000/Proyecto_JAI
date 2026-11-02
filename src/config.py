"""Carga de la configuración central (config/project.yaml)."""

from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "project.yaml"


def load_config(path: Path = CONFIG_PATH) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def project_path(relative: str) -> Path:
    """Resuelve una ruta de la sección `paths` relativa a la raíz del repositorio."""
    return PROJECT_ROOT / relative
