"""Tests del sitio bilingüe del stand (docs/index.html)."""

import json
import re

import pandas as pd
import pytest

from src.config import project_path

SITE = project_path("docs/index.html")


@pytest.fixture(scope="module")
def html():
    return SITE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def data(html):
    return json.loads(re.search(r"const DATA = (\{.*?\});\n", html, flags=re.S).group(1))


def test_sin_marcadores_sin_expandir(html):
    assert "[[es:" not in html
    assert "||pt:" not in html
    assert "{{" not in html
    assert "__DATOS__" not in html


def test_cada_texto_tiene_sus_dos_idiomas(html):
    assert html.count('class="es"') == html.count('class="pt"') > 50


def test_autonomo_sin_recursos_externos(html):
    # Debe cargar rápido y sin depender de otros sitios en la red del evento.
    assert not re.search(r'<(script|link|img)[^>]+(src|href)="http', html)


def test_cifras_coinciden_con_los_resultados(data):
    run = project_path("reports/runs/20261030-103735_modelos")
    reg = pd.read_csv(run / "regresion_metricas.csv")
    cls = pd.read_csv(run / "clasificacion_metricas.csv")
    r2 = reg[(reg["conjunto"] == "con_rezago") & (reg["modelo"] == "R2_persistencia")].iloc[0]
    c2 = cls[(cls["conjunto"] == "con_rezago") & (cls["modelo"] == "C2_persistencia_riesgo")].iloc[0]
    assert data["ref_regresion"] == pytest.approx(r2["MAE"])
    assert data["regresion"][1]["v"] == pytest.approx(r2["MAE"])
    assert data["clasificacion"][1]["v"] == pytest.approx(c2["balanced_accuracy"])
    assert len(data["regresion"]) == len(data["clasificacion"]) == 7


def test_mortalidad_coincide_con_el_panel(data):
    panel = pd.read_csv(project_path("data/processed/panel_departamento_ejercicio.csv"))
    assert data["anios"] == sorted(panel["AnioEjercicio"].unique().tolist())
    assert set(data["mortalidad"]) == set(panel["Departamento"])
    row = panel[(panel["Departamento"] == "Salto") & (panel["AnioEjercicio"] == 2024)].iloc[0]
    assert data["mortalidad"]["Salto"][data["anios"].index(2024)] == pytest.approx(row["tasa_mortalidad_1000"], abs=0.05)


def test_integrantes_y_logo_arriba_del_titulo(html):
    title = html.index("<h1>")
    for name in ["Luisa Gabriela Flores Piñeyro", "Alejandra Daiana Ramírez Sempert",
                 "Alvaro Martin Barreto Tacoronte", "Juan Pedro de León Sum"]:
        assert 0 < html.index(name) < title
    assert 0 < html.index('src="data:image/png;base64,') < title
    assert 'alt="UTEC, Universidad Tecnológica"' in html
