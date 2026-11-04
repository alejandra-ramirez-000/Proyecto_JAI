"""Genera el sitio bilingüe (español/portugués) del stand en docs/index.html.

Uso:
    python reports/sitio/build_sitio.py

Lee las cifras de los artefactos del proyecto, igual que el informe y el banner, y
expande la plantilla: cada `[[es:...||pt:...]]` se convierte en dos variantes, de las
que el navegador muestra solo la del idioma elegido. Es un único archivo, sin
dependencias externas, para publicar con GitHub Pages desde la carpeta docs/.
"""

import base64
import json
import re
from pathlib import Path

import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "reports/sitio/plantilla.tpl"
LOGOS = {"utec": ROOT / "reports/sitio/logo_utec.png", "jai": ROOT / "reports/sitio/logo_jai.png"}
OUTPUT_DIR = ROOT / "docs"
RUN_NAME = "20261030-103735_modelos"
RUN = ROOT / "reports/runs" / RUN_NAME

MODELS = [
    ("base", "R1_promedio_departamental", "C1_clase_mayoritaria",
     {"es": "Promedio del departamento", "pt": "Média do departamento"},
     {"es": "Clase mayoritaria", "pt": "Classe majoritária"}),
    ("base", "R2_persistencia", "C2_persistencia_riesgo",
     {"es": "Persistencia (año anterior)", "pt": "Persistência (ano anterior)"},
     {"es": "Persistencia del riesgo", "pt": "Persistência do risco"}),
    ("control", "ridge_H_sin_clima", "logistica_H_sin_clima",
     {"es": "Año anterior, sin clima", "pt": "Ano anterior, sem clima"},
     {"es": "Año anterior, sin clima", "pt": "Ano anterior, sem clima"}),
    ("climate", "ridge_A_ejercicio", "logistica_A_ejercicio",
     {"es": "Clima básico", "pt": "Clima básico"}, {"es": "Clima básico", "pt": "Clima básico"}),
    ("climate", "ridge_B_ejercicio", "logistica_B_ejercicio",
     {"es": "Chill Index", "pt": "Chill Index"}, {"es": "Chill Index", "pt": "Chill Index"}),
    ("climate", "ridge_C-A_ejercicio", "logistica_C-A_ejercicio",
     {"es": "Clima básico + año anterior", "pt": "Clima básico + ano anterior"},
     {"es": "Clima básico + año anterior", "pt": "Clima básico + ano anterior"}),
    ("climate", "ridge_C-B_ejercicio", "logistica_C-B_ejercicio",
     {"es": "Chill Index + año anterior", "pt": "Chill Index + ano anterior"},
     {"es": "Chill Index + año anterior", "pt": "Chill Index + ano anterior"}),
]


def comma(value: float, decimals: int) -> str:
    return f"{value:.{decimals}f}".replace(".", ",").replace("-", "−")


def figures() -> dict:
    df = pd.read_csv(ROOT / "reports/tables/informe_cifras.csv")
    return {key: value for key, value in zip(df["id"], df["valor"])}


def department_rows(panel: pd.DataFrame) -> list[dict]:
    rows = []
    for name, group in panel.groupby("Departamento"):
        station = group["EstacionAgr"].iloc[0].replace("Tacuarembó ", "").replace("Treinta y Tres ", "")
        stock = group["stock_ovino"] / 1000
        rows.append({
            "nombre": name,
            "estacion": station,
            "intensidad": f"{comma(group['intensidad_ug_ha'].mean(), 2)} ± {comma(group['intensidad_ug_ha'].std(), 2)}",
            "mortalidad": f"{comma(group['tasa_mortalidad_1000'].mean(), 1)} ± {comma(group['tasa_mortalidad_1000'].std(), 1)}",
            "stock": f"{comma(stock.mean(), 0)} ± {comma(stock.std(), 0)}",
        })
    return rows


def forest_rows() -> tuple[list[dict], list[dict], float]:
    reg = pd.read_csv(RUN / "regresion_metricas.csv")
    cls = pd.read_csv(RUN / "clasificacion_metricas.csv")

    def pick(table, model):
        row = table[(table["conjunto"] == "con_rezago") & (table["modelo"] == model)]
        if len(row) != 1:
            raise KeyError(model)
        return row.iloc[0]

    reg_rows, cls_rows = [], []
    for role, reg_model, cls_model, reg_label, cls_label in MODELS:
        r, c = pick(reg, reg_model), pick(cls, cls_model)
        reg_rows.append({"rol": role, "id": reg_model, **reg_label, "v": float(r["MAE"]), "lo": float(r["MAE_ic95_inf"]),
                         "hi": float(r["MAE_ic95_sup"])})
        cls_rows.append({"rol": role, "id": cls_model, **cls_label, "v": float(c["balanced_accuracy"]),
                         "lo": float(c["balanced_accuracy_ic95_inf"]), "hi": float(c["balanced_accuracy_ic95_sup"])})
    return reg_rows, cls_rows, float(pick(reg, "R2_persistencia")["MAE"])


def page_data(panel: pd.DataFrame, f: dict) -> dict:
    wide = panel.pivot(index="AnioEjercicio", columns="Departamento", values="tasa_mortalidad_1000").round(1)
    reg_rows, cls_rows, ref = forest_rows()
    return {
        "anios": [int(y) for y in wide.index],
        "mortalidad": {name: wide[name].tolist() for name in wide.columns},
        "mortalidad_media": wide.mean(axis=1).round(1).tolist(),
        "departamentos": department_rows(panel),
        "correlaciones": {
            var: {"global": float(f[f"r_mort_{var}_global"]), "intra": float(f[f"r_mort_{var}_intra"]),
                  "intra_anio": float(f[f"r_mort_{var}_intra_anio"])}
            for var in ("ci1000", "ci1200", "precip")
        },
        "regresion": reg_rows,
        "clasificacion": cls_rows,
        "ref_regresion": ref,
        "anomalias": anomalies(panel),
    }


def expand_languages(html: str) -> str:
    def replace(match):
        return f'<span class="es">{match.group(1)}</span><span class="pt">{match.group(2)}</span>'

    html, _ = re.subn(r"\[\[es:(.*?)\|\|pt:(.*?)\]\]", replace, html, flags=re.S)
    if "[[es:" in html or "||pt:" in html:
        raise ValueError("Quedó un marcador de idioma sin expandir")
    return html


def logo_tokens() -> dict:
    """Logos incrustados, para que el sitio siga siendo un único archivo."""
    tokens = {}
    for key, path in LOGOS.items():
        with Image.open(path) as image:
            tokens[f"logo_{key}_w"], tokens[f"logo_{key}_h"] = map(str, image.size)
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        tokens[f"logo_{key}"] = f"data:image/png;base64,{encoded}"
    return tokens


def anomalies(panel: pd.DataFrame) -> dict:
    """Valores y anomalías z por departamento y ejercicio, para el heatmap."""
    out = {}
    for key, column, decimals in [("mort", "tasa_mortalidad_1000", 1), ("ci", "dias_ci_ge_1000_ejercicio", 0),
                                  ("precip", "precip_total_mm_ejercicio", 0)]:
        wide = panel.pivot(index="Departamento", columns="AnioEjercicio", values=column).astype(float)
        z = wide.sub(wide.mean(axis=1), axis=0).div(wide.std(axis=1), axis=0)
        z.loc["Média"] = z.mean(axis=0)
        wide.loc["Média"] = wide.mean(axis=0)
        out[key] = {"dec": decimals,
                    "z": {name: [round(float(v), 2) for v in row] for name, row in z.iterrows()},
                    "raw": {name: [round(float(v), 1) for v in row] for name, row in wide.iterrows()}}
    return out


def build() -> Path:
    f = figures()
    panel = pd.read_csv(ROOT / "data/processed/panel_departamento_ejercicio.csv")
    tokens = {
        **logo_tokens(),
        "ba_c2": comma(float(f["C2_balanced_accuracy"]), 2),
        "panel_filas": str(int(float(f["panel_filas"]))),
        "especificaciones": str(int(float(f["especificaciones_evaluadas"]))),
        "skill": comma(abs(float(f["ridge_CA_skill_control"])) * 100, 0),
        "filas_ovinas": f"{int(float(f['filas_ovinas_alcance'])):,}".replace(",", "."),
        "r_int_lag": comma(float(f["r_int_lag_global"]), 2),
        "run": RUN_NAME,
    }
    html = TEMPLATE.read_text(encoding="utf-8")
    html = expand_languages(html)
    for key, value in tokens.items():
        html = html.replace("{{" + key + "}}", value)
    html = html.replace("/*__DATOS__*/null", json.dumps(page_data(panel, f), ensure_ascii=False))
    if "{{" in html:
        raise ValueError("Quedó un marcador de cifra sin reemplazar")
    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    return out


if __name__ == "__main__":
    print(f"Sitio escrito en {build()}")
