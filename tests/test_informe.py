"""Tests del informe final: cada cifra proviene de un artefacto guardado (sección 30, Fase 6)."""

import re

import pandas as pd
import pytest

from src.config import project_path
from src.reporting import informe_cifras

REPORT = project_path("reports/informe_final.md")


@pytest.fixture(scope="module")
def report_text():
    return REPORT.read_text(encoding="utf-8")


def test_cifras_se_regeneran_desde_los_artefactos():
    saved = pd.read_csv(project_path("reports/tables/informe_cifras.csv"))
    fresh = informe_cifras.collect()
    assert list(saved["id"]) == list(fresh["id"])
    for (_, a), (_, b) in zip(saved.iterrows(), fresh.iterrows()):
        assert str(a["valor"]) == str(b["valor"]) or float(a["valor"]) == pytest.approx(float(b["valor"])), a["id"]


def test_fuentes_de_las_cifras_existen():
    saved = pd.read_csv(project_path("reports/tables/informe_cifras.csv"))
    for source in saved["fuente"]:
        assert project_path(source.split(" [")[0]).is_file(), source


def test_corridas_citadas_existen(report_text):
    runs = set(re.findall(r"\d{8}-\d{6}_[a-z_]+", report_text))
    assert {informe_cifras.RUN_MODELS, informe_cifras.RUN_V10, informe_cifras.RUN_EXPLORATORY} <= runs
    for run in runs:
        assert project_path(f"reports/runs/{run}").is_dir(), run


def test_imagenes_enlazadas_existen(report_text):
    images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", report_text)
    assert images
    for image in images:
        assert (REPORT.parent / image).is_file(), image


def test_conclusion_coincide_con_los_criterios():
    cifras = pd.read_csv(project_path("reports/tables/informe_cifras.csv")).set_index("id")["valor"]
    assert int(cifras["regresion_principales_con_valor"]) == 0
    assert int(cifras["clasificacion_principales_con_valor"]) == 0
