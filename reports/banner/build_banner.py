"""Genera el banner académico (90 × 120 cm) sobre la plantilla oficial de la 41ª JAI–UFSM.

Uso (requiere python-pptx, ver requirements.txt):
    python reports/banner/build_banner.py

Lee las cifras de reports/tables/informe_cifras.csv y el panel procesado, para que
el banner cite exactamente los mismos números que el informe final.
"""

import copy
from pathlib import Path

import pandas as pd
from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_MARKER_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Cm, Pt

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "reports/banner/plantilla_JAI_90x120.pptx"
OUTPUT = ROOT / "reports/banner/banner_JAI_2026.pptx"

# Paleta tomada del logo de la JAI + tonos "hielo" para el tema del frío.
NAVY = RGBColor(0x00, 0x32, 0x55)
BLUE = RGBColor(0x00, 0x78, 0xB4)
ORANGE = RGBColor(0xF0, 0x7D, 0x00)
ICE = RGBColor(0xEC, 0xF3, 0xF9)
ICE_MID = RGBColor(0xC2, 0xD9, 0xED)
LINE_LIGHT = RGBColor(0x9D, 0xC3, 0xE0)
GRAY = RGBColor(0xA9, 0xB4, 0xBF)
TEXT = RGBColor(0x1B, 0x25, 0x33)
MUTED = RGBColor(0x55, 0x61, 0x70)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SCALE = [RGBColor(0xDC, 0xEA, 0xF5), RGBColor(0x9D, 0xC3, 0xE0), RGBColor(0x4F, 0x97, 0xC9),
         RGBColor(0x0B, 0x5E, 0x96), NAVY]
FONT = "Arial"
LINE_BREAK = "<br>"  # marcador de salto de línea dentro de un párrafo

MARGIN, GAP = 3.0, 1.4
CONTENT_W = 90.0 - 2 * MARGIN


# ---------------------------------------------------------------------------
# Datos
# ---------------------------------------------------------------------------

def load_figures() -> dict:
    df = pd.read_csv(ROOT / "reports/tables/informe_cifras.csv")
    out = {}
    for key, value in zip(df["id"], df["valor"]):
        try:
            out[key] = float(value)
        except ValueError:
            out[key] = value
    return out


def fmt(value: float, decimals: int) -> str:
    return f"{value:.{decimals}f}".replace(".", ",")


# ---------------------------------------------------------------------------
# Primitivas de dibujo
# ---------------------------------------------------------------------------

def _no_shadow(shape):
    shape.shadow.inherit = False


def box(slide, x, y, w, h, fill, radius=0.04, shape=MSO_SHAPE.ROUNDED_RECTANGLE, name=None, line=None):
    s = slide.shapes.add_shape(shape, Cm(x), Cm(y), Cm(w), Cm(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(2)
    _no_shadow(s)
    if name:
        s.name = name
    s.text_frame.text = ""
    return s


def text(slide, x, y, w, h, paragraphs, anchor=MSO_ANCHOR.TOP, name=None, margin=0.0):
    """paragraphs: lista de dicts {runs: [(texto, opciones)], align, space_after, bullet, line_spacing}."""
    tb = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Cm(margin))
    for i, para in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = para.get("align", PP_ALIGN.LEFT)
        if "space_after" in para:
            p.space_after = Pt(para["space_after"])
        if "space_before" in para:
            p.space_before = Pt(para["space_before"])
        if "line_spacing" in para:
            p.line_spacing = para["line_spacing"]
        if para.get("bullet"):
            _bullet(p, para.get("bullet_color", ORANGE), para.get("indent", 1.1))
        for run_text, opts in para["runs"]:
            r = p.add_run()
            r.text = run_text
            f = r.font
            f.name = FONT
            f.size = Pt(opts.get("size", 28))
            f.bold = opts.get("bold", False)
            f.italic = opts.get("italic", False)
            f.color.rgb = opts.get("color", TEXT)
            if opts.get("superscript"):
                r._r.get_or_add_rPr().set("baseline", "30000")
            if opts.get("spacing"):
                r._r.get_or_add_rPr().set("spc", str(opts["spacing"]))
    return tb


def _bullet(paragraph, color, indent_cm):
    pPr = paragraph._p.get_or_add_pPr()
    emu = int(Cm(indent_cm))
    pPr.set("marL", str(emu))
    pPr.set("indent", str(-emu))
    for tag in ("a:buClr", "a:buSzPct", "a:buFont", "a:buChar", "a:buNone"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    clr = etree.SubElement(pPr, qn("a:buClr"))
    srgb = etree.SubElement(clr, qn("a:srgbClr"))
    srgb.set("val", str(color))
    sz = etree.SubElement(pPr, qn("a:buSzPct"))
    sz.set("val", "100000")
    font = etree.SubElement(pPr, qn("a:buFont"))
    font.set("typeface", "Arial")
    char = etree.SubElement(pPr, qn("a:buChar"))
    char.set("char", "•")


def runs(markup: str, size=28, color=TEXT, bold_color=None):
    """'texto **negrita** texto' -> lista de runs."""
    out = []
    for i, part in enumerate(markup.split("**")):
        if not part:
            continue
        bold = i % 2 == 1
        out.append((part, {"size": size, "bold": bold, "color": (bold_color or color) if bold else color}))
    return out


def section_header(slide, number, title, x, y, w, dark=False):
    circle = box(slide, x, y, 2.3, 2.3, ORANGE, shape=MSO_SHAPE.OVAL, name=f"Número {number}")
    tf = circle.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = str(number)
    r.font.name, r.font.size, r.font.bold, r.font.color.rgb = FONT, Pt(40), True, WHITE
    text(slide, x + 3.0, y - 0.1, w - 3.0, 2.5,
         [{"runs": [(title, {"size": 46, "bold": True, "color": WHITE if dark else NAVY})]}],
         anchor=MSO_ANCHOR.MIDDLE, name=f"Título sección {number}")


def card(slide, number, title, x, y, w, h, fill=ICE, dark=False):
    box(slide, x, y, w, h, fill, radius=0.035, name=f"Tarjeta {number}")
    section_header(slide, number, title, x + 1.2, y + 1.1, w - 2.4, dark=dark)
    return x + 1.2, y + 4.3, w - 2.4  # origen y ancho del contenido


def arrow_down(slide, x, y, h, color=BLUE):
    a = box(slide, x - 0.6, y, 1.2, h, color, shape=MSO_SHAPE.DOWN_ARROW, name="Flecha")
    return a


def style_chart_text(chart, size=22):
    chart.font.name = FONT
    chart.font.size = Pt(size)
    chart.font.color.rgb = TEXT


def quiet_axes(chart, value_max=None, value_min=0.0, number_format=None, show_value_labels=False):
    va = chart.value_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = ICE_MID
    va.major_gridlines.format.line.width = Pt(1)
    va.format.line.fill.background()
    va.visible = show_value_labels
    va.minimum_scale = value_min
    if value_max is not None:
        va.maximum_scale = value_max
    if number_format:
        va.tick_labels.number_format = number_format
        va.tick_labels.number_format_is_linked = False
    va.tick_labels.font.color.rgb = MUTED
    ca = chart.category_axis
    ca.format.line.color.rgb = GRAY
    ca.has_major_gridlines = False
    ca.tick_labels.font.color.rgb = TEXT


# ---------------------------------------------------------------------------
# Encabezado de la plantilla
# ---------------------------------------------------------------------------

def fill_header(slide):
    # Quitar los cuadros vacíos de la plantilla (grupo con un rectángulo sin texto ni relleno).
    for shape in list(slide.shapes):
        if shape.shape_type == 6 or (shape.has_text_frame and not shape.text_frame.text.strip()):
            shape._element.getparent().remove(shape._element)

    header = next(s for s in slide.shapes if s.has_text_frame and "Jornada" in s.text_frame.text)
    paragraphs = header.text_frame.paragraphs
    # Párrafos: 0 título de la Jornada, 1 vacío, 2 área, 3 título del trabajo, 4 autores.
    for p in paragraphs:
        pPr = p._p.get_or_add_pPr()
        if pPr.find(qn("a:buNone")) is None:
            etree.SubElement(pPr, qn("a:buNone"))

    def set_runs(p, items):
        for child in list(p._p):
            if child.tag in (qn("a:r"), qn("a:br")):
                p._p.remove(child)
        for content, opts in items:
            if content == LINE_BREAK:
                p.add_line_break()
                continue
            r = p.add_run()
            r.text = content
            r.font.name = FONT
            r.font.size = Pt(opts.get("size", 32))
            r.font.bold = opts.get("bold", False)
            r.font.color.rgb = opts.get("color", TEXT)
            if opts.get("underline"):
                r.font.underline = True
            if opts.get("superscript"):
                r._r.get_or_add_rPr().set("baseline", "30000")

    set_runs(paragraphs[2], [("CIÊNCIAS AGRÁRIAS", {"size": 28, "color": BLUE, "bold": True}),
                             ("  ·  AGRONOMIA / AGROMETEOROLOGIA", {"size": 28, "color": BLUE})])
    set_runs(paragraphs[3], [("SISTEMA PREDITIVO AGROCLIMÁTICO DE INTENSIDADE PECUÁRIA E RISCO DE MORTALIDADE",
                              {"size": 40, "bold": True, "color": NAVY})])
    authors = [("Luisa Gabriela Flores Piñeyro", {"underline": True}), ("1", {"superscript": True}),
               ("; Alejandra Daiana Ramírez Sempert", {}), ("1", {"superscript": True}),
               (";", {}), (LINE_BREAK, {}), ("Alvaro Martin Barreto Tacoronte", {}), ("1", {"superscript": True}),
               ("; Juan Pedro de León Sum", {}), ("1", {"superscript": True})]
    set_runs(paragraphs[4], [(t, {"size": 24, **o}) for t, o in authors])
    institution = copy.deepcopy(paragraphs[4]._p)
    paragraphs[4]._p.addnext(institution)
    inst_p = header.text_frame.paragraphs[5]
    set_runs(inst_p, [("1", {"size": 21, "superscript": True, "color": MUTED}),
                      ("Universidad Tecnológica del Uruguay (UTEC) · Licenciatura en Ingeniería de Datos e "
                       "Inteligencia Artificial", {"size": 21, "color": MUTED})])
    # El párrafo vacío entre la Jornada y el área queda como separador fino.
    end = paragraphs[1]._p.find(qn("a:endParaRPr"))
    if end is not None:
        end.set("sz", "1200")


# ---------------------------------------------------------------------------
# Bloques del banner
# ---------------------------------------------------------------------------

def hero(slide, f, y):
    h = 14.6
    box(slide, MARGIN, y, CONTENT_W, h, NAVY, radius=0.06, name="Bloque principal")
    left_w = 44.0
    text(slide, MARGIN + 2.0, y + 1.4, left_w, 7.6, [
        {"runs": [("A PERGUNTA", {"size": 26, "bold": True, "color": ORANGE, "spacing": 300})], "space_after": 10},
        {"runs": [("O clima e o Chill Index preveem a intensidade pecuária e a mortalidade ovina melhor do que "
                   "a própria história de cada departamento?", {"size": 44, "bold": True, "color": WHITE})],
         "line_spacing": 1.05},
    ], name="Pergunta")
    right_x = MARGIN + 2.0 + left_w + 2.5
    text(slide, right_x, y + 1.4, CONTENT_W - (right_x - MARGIN) - 2.0, 7.6, [
        {"runs": [("A RESPOSTA", {"size": 26, "bold": True, "color": ORANGE, "spacing": 300})], "space_after": 10},
        {"runs": [("Não. ", {"size": 60, "bold": True, "color": ORANGE}),
                  ("Com 9 anos de dados, nenhum modelo climático supera de forma robusta a persistência de cada "
                   "departamento.",
                   {"size": 36, "color": WHITE})], "line_spacing": 1.05},
    ], name="Resposta")

    stats = [
        (f"{int(f['panel_filas'])}", "observações\n5 departamentos × 9 anos"),
        (f"{int(f['especificaciones_evaluadas'])}", "modelos avaliados\nfora da amostra"),
        (f"{int(f['regresion_principales_con_valor'] + f['clasificacion_principales_con_valor'])}",
         "modelos climáticos\nprincipais com valor preditivo"),
        (fmt(f["C2_balanced_accuracy"], 2), "acurácia da persistência\no melhor preditor"),
    ]
    sw = (CONTENT_W - 4.0) / len(stats)
    for i, (number, label) in enumerate(stats):
        sx = MARGIN + 2.0 + i * sw
        # Ancho aproximado de la cifra en Arial negrita de 96 pt: 1,9 cm por dígito, 0,95 cm por coma.
        number_w = sum(0.95 if ch == "," else 1.9 for ch in number) + 0.4
        text(slide, sx, y + 8.9, number_w, 4.4, [{"runs": [(number, {"size": 96, "bold": True, "color": ORANGE})]}],
             anchor=MSO_ANCHOR.MIDDLE, name=f"Cifra {i + 1}")
        lines = label.split("\n")
        text(slide, sx + number_w + 0.6, y + 9.4, sw - number_w - 1.0, 3.4,
             [{"runs": [(lines[0], {"size": 24, "bold": True, "color": WHITE})]},
              {"runs": [(lines[1], {"size": 24, "color": ICE_MID})]}],
             anchor=MSO_ANCHOR.MIDDLE, name=f"Etiqueta cifra {i + 1}")
    return y + h


def card_context(slide, x, y, w, h):
    cx, cy, cw = card(slide, 1, "Contexto e objetivo", x, y, w, h)
    text(slide, cx, cy, cw, h - 5.0, [
        {"runs": runs("O frio, o vento e a chuva aumentam a perda de calor dos ovinos. O INIA resume essa "
                      "exposição no **Chill Index**, usado para alertar sobre risco em cordeiros "
                      "recém-nascidos e ovinos pós-tosquia.", bold_color=NAVY), "space_after": 18},
        {"runs": runs("**Objetivo:** avaliar, fora da amostra, se o clima melhora a previsão anual de:",
                      bold_color=NAVY), "space_after": 8},
        {"runs": runs("**Intensidade pecuária** (UG/ha), por regressão", bold_color=NAVY), "bullet": True,
         "space_after": 6},
        {"runs": runs("**Mortalidade ovina elevada** (acima do percentil 75 do departamento), por classificação",
                      bold_color=NAVY), "bullet": True, "space_after": 18},
        {"runs": runs("Canelones · Colonia · Salto · Tacuarembó · Treinta y Tres, exercícios 2017–2025 "
                      "(julho a junho)", size=24, color=MUTED)},
    ], name="Texto contexto")


def card_data(slide, f, x, y, w, h):
    cx, cy, cw = card(slide, 2, "Dados e painel", x, y, w, h)
    bw = (cw - 1.2) / 2
    sources = [
        ("INIA", "dados diários · 5 estações", "temperatura, chuva e vento"),
        ("SNIG / DICOSE", "declarações anuais", "mortes, estoque, UG e área"),
    ]
    for i, (title, line1, line2) in enumerate(sources):
        bx = cx + i * (bw + 1.2)
        box(slide, bx, cy, bw, 4.4, WHITE, radius=0.08, name=f"Fonte {title}")
        text(slide, bx + 0.6, cy + 0.2, bw - 1.2, 4.0, [
            {"runs": [(title, {"size": 30, "bold": True, "color": NAVY})], "align": PP_ALIGN.CENTER,
             "space_after": 4},
            {"runs": [(line1, {"size": 22, "color": TEXT})], "align": PP_ALIGN.CENTER},
            {"runs": [(line2, {"size": 22, "color": MUTED})], "align": PP_ALIGN.CENTER},
        ], anchor=MSO_ANCHOR.MIDDLE, name=f"Texto fonte {title}")
        arrow_down(slide, bx + bw / 2, cy + 4.7, 1.0)
    steps = ["Chill Index diário\n+ agregação por exercício", "soma por departamento\n× exercício"]
    for i, step in enumerate(steps):
        bx = cx + i * (bw + 1.2)
        box(slide, bx, cy + 6.0, bw, 3.0, ICE_MID, radius=0.1, name=f"Etapa {i + 1}")
        lines = step.split("\n")
        text(slide, bx + 0.4, cy + 6.0, bw - 0.8, 3.0,
             [{"runs": [(lines[0], {"size": 22, "bold": True, "color": NAVY})], "align": PP_ALIGN.CENTER},
              {"runs": [(lines[1], {"size": 22, "color": NAVY})], "align": PP_ALIGN.CENTER}],
             anchor=MSO_ANCHOR.MIDDLE, name=f"Texto etapa {i + 1}")
        arrow_down(slide, bx + bw / 2, cy + 9.3, 1.0)
    panel_y = cy + 10.6
    box(slide, cx, panel_y, cw, 3.8, NAVY, radius=0.1, name="Painel")
    text(slide, cx + 0.8, panel_y, cw - 1.6, 3.8, [
        {"runs": [(f"Painel: {int(f['panel_filas'])} observações", {"size": 32, "bold": True, "color": WHITE})],
         "align": PP_ALIGN.CENTER},
        {"runs": [(f"departamento × exercício · {int(f['panel_filas_rezago'])} com o ano anterior",
                   {"size": 22, "color": ICE_MID})], "align": PP_ALIGN.CENTER},
    ], anchor=MSO_ANCHOR.MIDDLE, name="Texto painel")
    text(slide, cx, panel_y + 4.3, cw, 2.6, [
        {"runs": runs(f"Auditoria automática: **{int(f['auditoria_chequeos_ok'])}/{int(f['auditoria_chequeos_total'])}"
                      "** verificações; valores mascarados e negativos detectados e controlados.",
                      size=22, color=MUTED, bold_color=NAVY)},
    ], name="Texto auditoria")


def card_chill(slide, f, x, y, w, h):
    cx, cy, cw = card(slide, 3, "Chill Index (INIA)", x, y, w, h)
    box(slide, cx, cy, cw, 6.2, WHITE, radius=0.08, name="Fórmula")
    text(slide, cx + 0.8, cy + 0.3, cw - 1.6, 5.6, [
        {"runs": [("CI = (11,7 + 3,1·√VV)·(40 − Ta) + 481 + R", {"size": 28, "bold": True, "color": NAVY})],
         "align": PP_ALIGN.CENTER, "space_after": 6},
        {"runs": [("R = 418·(1 − e", {"size": 28, "bold": True, "color": NAVY}),
                  ("−0,04·P", {"size": 28, "bold": True, "color": NAVY, "superscript": True}),
                  (")", {"size": 28, "bold": True, "color": NAVY})], "align": PP_ALIGN.CENTER, "space_after": 10},
        {"runs": [("VV vento (m/s) · Ta temperatura média (°C) · P chuva (mm)",
                   {"size": 20, "color": MUTED})], "align": PP_ALIGN.CENTER},
        {"runs": [("CI: perda potencial de calor, em kJ/m²/h", {"size": 20, "color": MUTED})],
         "align": PP_ALIGN.CENTER},
    ], anchor=MSO_ANCHOR.MIDDLE, name="Texto fórmula")

    labels = [("< 900", "sem risco"), ("900", "baixo"), ("1000", "médio"), ("1100", "alto"), ("≥ 1200", "crítico")]
    sy = cy + 7.4
    segment = cw / len(labels)
    for i, ((value, name), color) in enumerate(zip(labels, SCALE)):
        sx = cx + i * segment
        seg = box(slide, sx, sy, segment - 0.15, 2.6, color, radius=0.12, name=f"Escala {name}")
        ink = NAVY if i < 2 else WHITE
        text(slide, sx, sy, segment - 0.15, 2.6, [{"runs": [(value, {"size": 26, "bold": True, "color": ink})],
                                                    "align": PP_ALIGN.CENTER}],
             anchor=MSO_ANCHOR.MIDDLE, name=f"Valor escala {name}")
        text(slide, sx, sy + 2.8, segment - 0.15, 1.4, [{"runs": [(name, {"size": 22, "color": TEXT})],
                                                          "align": PP_ALIGN.CENTER}], name=f"Nome escala {name}")
    text(slide, cx, sy + 5.0, cw, h - (sy + 5.0 - y) - 1.0, [
        {"runs": runs("Por exercício: **dias com CI ≥ 1000 e ≥ 1200**, CI máximo e percentil 95, em duas "
                      "janelas: exercício completo e **julho–outubro** (parições).", size=26, bold_color=NAVY),
         "space_after": 14},
        {"runs": runs(f"Cobertura climática **≥ {fmt(f['cobertura_min_jul_oct'] * 100, 1)} %** dos dias em todos os "
                      f"exercícios; {int(f['dias_sin_ci'])} dias sem CI, nenhum imputado.", size=22, color=MUTED,
                      bold_color=NAVY)},
    ], name="Texto variáveis CI")


def card_validation(slide, x, y, w, h):
    cx, cy, cw = card(slide, 4, "Validação sem vazamento", x, y, w, h)
    years = list(range(2017, 2026))
    cell, gap = 1.08, 0.2
    gx, gy = cx + 2.6, cy + 1.2
    text(slide, gx, cy, 9 * (cell + gap), 1.3, [{"runs": [("exercício usado →", {"size": 20, "color": MUTED})]}],
         name="Rótulo colunas")
    for i, year in enumerate(years):
        text(slide, gx + i * (cell + gap) - 0.2, gy - 0.05, cell + 0.4, 1.0,
             [{"runs": [(f"’{str(year)[2:]}", {"size": 18, "color": MUTED})], "align": PP_ALIGN.CENTER}],
             name=f"Ano {year}")
    for r, test_year in enumerate(years):
        ry = gy + 1.1 + r * (cell + gap)
        text(slide, cx, ry - 0.05, 2.4, cell + 0.1,
             [{"runs": [(f"’{str(test_year)[2:]}", {"size": 18, "bold": True, "color": ORANGE})],
               "align": PP_ALIGN.RIGHT}], anchor=MSO_ANCHOR.MIDDLE, name=f"Partição {test_year}")
        for c, year in enumerate(years):
            fill = ORANGE if year == test_year else ICE_MID
            box(slide, gx + c * (cell + gap), ry, cell, cell, fill, radius=0.18, name=f"Célula {test_year}-{year}")
    legend_y = gy + 1.1 + 9 * (cell + gap) + 0.4
    for i, (label, color) in enumerate([("previsto (teste)", ORANGE), ("treino", ICE_MID)]):
        lx = gx + i * 7.0
        box(slide, lx, legend_y + 0.25, 0.9, 0.9, color, radius=0.18, name=f"Legenda {label}")
        text(slide, lx + 1.2, legend_y, 5.6, 1.4, [{"runs": [(label, {"size": 20, "color": TEXT})]}],
             anchor=MSO_ANCHOR.MIDDLE, name=f"Texto legenda {label}")

    tx = gx + 9 * (cell + gap) + 1.4
    text(slide, tx, cy, cw - (tx - cx), h - 5.0, [
        {"runs": runs("**Leave-One-Year-Out:** cada exercício é previsto sem ter sido visto; os 5 departamentos "
                      "do ano ficam fora juntos.", size=26, bold_color=NAVY), "space_after": 14},
        {"runs": runs("Limiar P75 de mortalidade recalculado **só com o treino**", size=26, bold_color=NAVY),
         "bullet": True, "space_after": 8},
        {"runs": runs("Padronização e hiperparâmetros **dentro de cada partição**", size=26, bold_color=NAVY),
         "bullet": True, "space_after": 8},
        {"runs": runs("Comparação com **baselines**: média do departamento e persistência (ano anterior)",
                      size=26, bold_color=NAVY), "bullet": True, "space_after": 8},
        {"runs": runs("**Controle sem clima:** só o ano anterior", size=26, bold_color=NAVY), "bullet": True,
         "space_after": 14},
        {"runs": runs("Ridge (regressão) · logística L2 (classificação)", size=22, color=MUTED)},
    ], name="Texto validação")


def card_mortality(slide, panel, x, y, w, h):
    cx, cy, cw = card(slide, 5, "Os departamentos se movem juntos", x, y, w, h)
    data = panel.pivot(index="AnioEjercicio", columns="Departamento", values="tasa_mortalidad_1000")
    chart_data = CategoryChartData()
    chart_data.categories = [str(y) for y in data.index]
    for dept in data.columns:
        chart_data.add_series(dept, [round(v, 1) for v in data[dept]])
    chart_data.add_series("Média dos 5 departamentos", [round(v, 1) for v in data.mean(axis=1)])
    gf = slide.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Cm(cx - 0.4), Cm(cy - 0.3), Cm(cw + 0.4), Cm(h - 9.6),
                                chart_data)
    gf.name = "Gráfico mortalidade"
    chart = gf.chart
    style_chart_text(chart, 22)
    chart.has_title = False
    chart.has_legend = False
    quiet_axes(chart, value_max=120, value_min=20, number_format="0", show_value_labels=True)
    chart.value_axis.major_unit = 20
    for i, series in enumerate(chart.series):
        series.smooth = False
        mean = i == len(chart.series) - 1
        series.format.line.color.rgb = NAVY if mean else LINE_LIGHT
        series.format.line.width = Pt(6 if mean else 2.25)
        series.marker.style = XL_MARKER_STYLE.CIRCLE if mean else XL_MARKER_STYLE.NONE
        if mean:
            series.marker.size = 14
            series.marker.format.fill.solid()
            series.marker.format.fill.fore_color.rgb = NAVY
            series.marker.format.line.color.rgb = WHITE
    text(slide, cx, y + h - 5.4, cw, 4.6, [
        {"runs": runs("Mortes por mil ovinos. **Linha escura: média;** linhas claras: cada departamento. "
                      "Queda comum em **2021–2023** e alta em **2024–2025**: o sinal está no ano, não na região.",
                      size=24, color=TEXT, bold_color=NAVY)},
    ], name="Texto mortalidade")


def bar_chart(slide, x, y, w, h, categories, values, colors, number_format, value_max, name):
    chart_data = CategoryChartData()
    chart_data.categories = categories
    chart_data.add_series("valor", values)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Cm(x), Cm(y), Cm(w), Cm(h), chart_data)
    gf.name = name
    chart = gf.chart
    style_chart_text(chart, 22)
    chart.has_title = False
    chart.has_legend = False
    plot = chart.plots[0]
    plot.gap_width = 45
    plot.vary_by_categories = False
    quiet_axes(chart, value_max=value_max, number_format=number_format)
    chart.category_axis.reverse_order = True
    chart.category_axis.tick_labels.font.size = Pt(22)
    series = plot.series[0]
    for idx, color in enumerate(colors):
        point = series.points[idx]
        point.format.fill.solid()
        point.format.fill.fore_color.rgb = color
        point.format.line.fill.background()
    plot.has_data_labels = True
    labels = plot.data_labels
    labels.number_format = number_format
    labels.number_format_is_linked = False
    labels.position = XL_LABEL_POSITION.OUTSIDE_END
    labels.font.size = Pt(24)
    labels.font.bold = True
    labels.font.color.rgb = TEXT
    return chart


def legend_chips(slide, x, y, items):
    cursor = x
    for label, color in items:
        box(slide, cursor, y + 0.3, 1.1, 1.1, color, radius=0.2, name=f"Chip {label}")
        width = 0.62 * len(label) + 1.0
        text(slide, cursor + 1.4, y, width, 1.7, [{"runs": [(label, {"size": 24, "color": TEXT})]}],
             anchor=MSO_ANCHOR.MIDDLE, name=f"Texto chip {label}")
        cursor += 1.4 + width + 0.6


def card_results(slide, f, x, y, w, h):
    cx, cy, cw = card(slide, 6, "Resultados fora da amostra (40 observações, 2018–2025)", x, y, w, h)
    legend_chips(slide, cx, cy - 0.4, [("baseline", GRAY), ("sem clima", NAVY), ("com clima", ORANGE)])
    half = (cw - 2.0) / 2
    top = cy + 1.8
    chart_h = h - (top - y) - 6.2

    reg = [
        ("Só o ano anterior (controle)", f["ridge_H_MAE"], NAVY),
        ("Persistência (baseline)", f["R2_MAE"], GRAY),
        ("CI + ano anterior", f["ridge_CB_MAE"], ORANGE),
        ("Clima básico + ano anterior", f["ridge_CA_MAE"], ORANGE),
        ("Média do departamento (baseline)", f["R1_rezago_MAE"], GRAY),
        ("Chill Index", f["ridge_B_rezago_MAE"], ORANGE),
        ("Clima básico", f["ridge_A_rezago_MAE"], ORANGE),
    ]
    text(slide, cx, top, half, 2.0, [
        {"runs": [("Intensidade pecuária", {"size": 32, "bold": True, "color": NAVY}),
                  ("  erro absoluto médio, UG/ha (menor é melhor)", {"size": 24, "color": MUTED})]},
    ], name="Título gráfico regressão")
    bar_chart(slide, cx - 0.3, top + 2.0, half + 0.3, chart_h, [r[0] for r in reg], [round(r[1], 4) for r in reg],
              [r[2] for r in reg], "0.0000", 0.03, "Gráfico regressão")

    cls = [
        ("Persistência do risco (baseline)", f["C2_balanced_accuracy"], GRAY),
        ("Só o ano anterior (controle)", f["log_H_balanced_accuracy"], NAVY),
        ("Clima básico + ano anterior", f["log_CA_balanced_accuracy"], ORANGE),
        ("Classe majoritária (acaso)", 0.5, GRAY),
        ("Clima básico", f["log_A_rezago_balanced_accuracy"], ORANGE),
        ("CI + ano anterior", f["log_CB_balanced_accuracy"], ORANGE),
        ("Chill Index", f["log_B_rezago_balanced_accuracy"], ORANGE),
    ]
    rx = cx + half + 2.0
    text(slide, rx, top, half, 2.0, [
        {"runs": [("Mortalidade elevada", {"size": 32, "bold": True, "color": NAVY}),
                  ("  acurácia balanceada (0,5 = acaso)", {"size": 24, "color": MUTED})]},
    ], name="Título gráfico classificação")
    bar_chart(slide, rx - 0.3, top + 2.0, half + 0.3, chart_h, [c[0] for c in cls], [round(c[1], 2) for c in cls],
              [c[2] for c in cls], "0.00", 0.9, "Gráfico classificação")

    takeaway_y = y + h - 4.0
    skill = abs(f["ridge_CA_skill_control"]) * 100
    for i, (big, small) in enumerate([
        (f"+{fmt(skill, 0)} %", "de erro ao adicionar clima ao modelo que usa só o ano anterior"),
        (f"{fmt(f['log_B_rezago_balanced_accuracy'], 2)}–{fmt(f['log_CB_balanced_accuracy'], 2)}",
         "acurácia dos modelos com Chill Index: abaixo do acaso"),
    ]):
        tx = cx + i * (half + 2.0)
        box(slide, tx, takeaway_y, half, 3.0, WHITE, radius=0.12, name=f"Destaque {i + 1}")
        text(slide, tx + 0.8, takeaway_y, half - 1.6, 3.0, [
            {"runs": [(big + "  ", {"size": 44, "bold": True, "color": ORANGE}),
                      (small, {"size": 26, "color": TEXT})]},
        ], anchor=MSO_ANCHOR.MIDDLE, name=f"Texto destaque {i + 1}")


def card_why(slide, f, x, y, w, h):
    cx, cy, cw = card(slide, 7, "Por que o clima não prevê", x, y, w, h)
    chart_data = CategoryChartData()
    chart_data.categories = ["Dias CI ≥ 1000", "Dias CI ≥ 1200", "Precipitação"]
    for label, key in [("global", "global"), ("dentro do departamento", "intra"),
                       ("dentro do departamento e do ano", "intra_anio")]:
        chart_data.add_series(label, [f[f"r_mort_{v}_{key}"] for v in ("ci1000", "ci1200", "precip")])
    chart_w = cw * 0.58
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Cm(cx - 0.3), Cm(cy - 0.6), Cm(chart_w),
                                Cm(h - 4.6), chart_data)
    gf.name = "Gráfico correlações"
    chart = gf.chart
    style_chart_text(chart, 20)
    chart.has_title = False
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.legend.include_in_layout = False
    chart.legend.font.size = Pt(20)
    plot = chart.plots[0]
    plot.gap_width = 60
    plot.overlap = -10
    quiet_axes(chart, value_max=0.6, number_format="0.0")
    for series, color in zip(plot.series, [GRAY, BLUE, ORANGE]):
        series.format.fill.solid()
        series.format.fill.fore_color.rgb = color
        series.format.line.fill.background()
    plot.has_data_labels = True
    labels = plot.data_labels
    labels.number_format = "0.00"
    labels.number_format_is_linked = False
    labels.position = XL_LABEL_POSITION.OUTSIDE_END
    labels.font.size = Pt(20)
    labels.font.bold = True
    tx = cx + chart_w + 0.6
    text(slide, tx, cy, cw - (tx - cx), h - 5.0, [
        {"runs": runs("Correlação com a mortalidade (r de Pearson).", size=22, color=MUTED), "space_after": 12},
        {"runs": runs("A associação existe, mas vem de **choques comuns** a todos os departamentos no mesmo "
                      "ano.", size=26, bold_color=NAVY), "space_after": 12},
        {"runs": runs("Descontado o ano, **quase desaparece**: na prática há ~9 anos de informação, não 45.",
                      size=26, bold_color=NAVY)},
    ], name="Texto por quê")


def card_conclusions(slide, x, y, w, h):
    cx, cy, cw = card(slide, 8, "Conclusões", x, y, w, h, fill=NAVY, dark=True)
    items = [
        "Com a resolução disponível, **o clima e o Chill Index não melhoram de forma robusta** a previsão "
        "fora da amostra.",
        "**A história de cada departamento** é o melhor preditor.",
        "Resultado **robusto**: se mantém com outro critério de seleção, hiperparâmetros fixos e "
        "janela julho–outubro.",
        "**Próximo passo:** mortalidade datada e por categoria (cordeiros) e séries mais longas.",
    ]
    row_h = (h - 5.2) / len(items)
    for i, item in enumerate(items):
        ry = cy + i * row_h
        text(slide, cx, ry, 2.2, row_h, [{"runs": [(str(i + 1), {"size": 48, "bold": True, "color": ORANGE})]}],
             name=f"Número conclusão {i + 1}")
        text(slide, cx + 2.4, ry + 0.25, cw - 2.4, row_h, [
            {"runs": runs(item, size=26, color=WHITE, bold_color=WHITE)}], name=f"Conclusão {i + 1}")


def footer(slide, y):
    text(slide, MARGIN, y, CONTENT_W, 2.6, [
        {"runs": runs("**Limitações:** mortalidade anual sem data nem categoria · uma estação por departamento · "
                      "estoque declarado no fechamento · dados observacionais (sem inferência causal).",
                      size=20, color=MUTED, bold_color=TEXT), "space_after": 4},
        {"runs": runs("**Referências:** INIA. Previsão para cordeiros (Chill Index). · MGAP. Declaração jurada "
                      "DICOSE / SNIG. · Nixon-Smith, W. F. (1972). Bureau of Meteorology, Working Paper 150.",
                      size=20, color=MUTED, bold_color=TEXT)},
    ], name="Rodapé")


# ---------------------------------------------------------------------------

def build() -> Path:
    f = load_figures()
    panel = pd.read_csv(ROOT / "data/processed/panel_departamento_ejercicio.csv")
    prs = Presentation(str(TEMPLATE))
    slide = prs.slides[0]
    fill_header(slide)

    y = hero(slide, f, 14.4) + GAP
    col3 = (CONTENT_W - 2 * GAP) / 3
    row_a = 22.8
    card_context(slide, MARGIN, y, col3, row_a)
    card_data(slide, f, MARGIN + col3 + GAP, y, col3, row_a)
    card_chill(slide, f, MARGIN + 2 * (col3 + GAP), y, col3, row_a)
    y += row_a + GAP

    col2 = (CONTENT_W - GAP) / 2
    row_b = 21.6
    card_validation(slide, MARGIN, y, col2, row_b)
    card_mortality(slide, panel, MARGIN + col2 + GAP, y, col2, row_b)
    y += row_b + GAP

    row_c = 21.4
    card_results(slide, f, MARGIN, y, CONTENT_W, row_c)
    y += row_c + GAP

    row_d = 15.6
    card_why(slide, f, MARGIN, y, col2, row_d)
    card_conclusions(slide, MARGIN + col2 + GAP, y, col2, row_d)
    y += row_d + 0.9
    footer(slide, y)

    prs.save(str(OUTPUT))
    return OUTPUT


if __name__ == "__main__":
    print(f"Banner escrito en {build()}")
