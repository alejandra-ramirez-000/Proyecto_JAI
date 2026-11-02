import pytest

from src.config import load_config
from src.data.build_panel import build_panel
from src.data.load_inia import load_inia
from src.data.load_snig import load_animales, load_generales


@pytest.fixture(scope="session")
def cfg():
    return load_config()


@pytest.fixture(scope="session")
def animales():
    return load_animales()


@pytest.fixture(scope="session")
def generales():
    return load_generales()


@pytest.fixture(scope="session")
def inia():
    return load_inia()


@pytest.fixture(scope="session")
def panel_tables(cfg):
    return build_panel(cfg)


@pytest.fixture(scope="session")
def panel(panel_tables):
    return panel_tables["panel"]
