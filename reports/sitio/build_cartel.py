"""Genera el QR del sitio y un cartel A4 bilingüe para imprimir y poner en el stand.

Uso (requiere python-pptx y segno, ver requirements.txt):
    python reports/sitio/build_cartel.py

Escribe en reports/sitio/: qr_sitio.png, qr_sitio.svg (vectorial, para cualquier
tamaño de impresión) y cartel_stand.pptx. El logo sale de la plantilla oficial de la JAI.
"""

from io import BytesIO
from pathlib import Path

import segno
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Cm, Pt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports/sitio"
TEMPLATE = ROOT / "reports/banner/plantilla_JAI_90x120.pptx"
SITE_URL = "https://alejandra-ramirez-000.github.io/Proyecto_JAI/"

FONT = "Times New Roman"
INK = RGBColor(0x00, 0x32, 0x55)
BLACK = RGBColor(0x11, 0x11, 0x11)
MUTED = RGBColor(0x44, 0x44, 0x44)
PAGE_W, PAGE_H = 21.0, 29.7


def write_qr() -> Path:
    # Corrección de errores alta: se sigue leyendo aunque el cartel se raye o se doble.
    qr = segno.make(SITE_URL, error="h", boost_error=True)
    qr.save(str(OUT / "qr_sitio.svg"), scale=10, border=4, dark="#000", light="#fff")
    png = OUT / "qr_sitio.png"
    qr.save(str(png), scale=40, border=4)
    return png


def jai_logo() -> BytesIO:
    prs = Presentation(str(TEMPLATE))
    pictures = [s for s in prs.slides[0].shapes if s.shape_type == 13]
    logo = max(pictures, key=lambda s: s.width)  # el logo de la JAI es el más ancho de la plantilla
    return BytesIO(logo.image.blob)


def add_text(slide, x, y, w, h, runs, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, name=None):
    box = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    if name:
        box.name = name
    frame = box.text_frame
    frame.word_wrap = True
    frame.vertical_anchor = anchor
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    for content, size, bold, italic, color in runs:
        run = paragraph.add_run()
        run.text = content
        run.font.name, run.font.size, run.font.bold, run.font.italic = FONT, Pt(size), bold, italic
        run.font.color.rgb = color
    return box


def rule(slide, y, x1=2.0, x2=PAGE_W - 2.0, width=1.25):
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Cm(x1), Cm(y), Cm(x2), Cm(y))
    line.line.color.rgb = INK
    line.line.width = Pt(width)
    line.shadow.inherit = False
    line.name = "Filete"


def build() -> Path:
    qr_png = write_qr()
    prs = Presentation()
    prs.slide_width, prs.slide_height = Cm(PAGE_W), Cm(PAGE_H)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    logo_w = 7.0
    slide.shapes.add_picture(jai_logo(), Cm((PAGE_W - logo_w) / 2), Cm(1.3), width=Cm(logo_w)).name = "Logo JAI"

    add_text(slide, 2, 4.2, 17, 1.5, [("¿Querés saber más?", 38, True, False, INK)], name="Título ES")
    add_text(slide, 2, 5.7, 17, 1.4, [("Quer saber mais?", 34, True, True, INK)], name="Título PT")
    rule(slide, 7.5)

    qr_size = 13.0
    slide.shapes.add_picture(str(qr_png), Cm((PAGE_W - qr_size) / 2), Cm(7.9), Cm(qr_size), Cm(qr_size)).name = "QR sitio"
    rule(slide, 21.3)

    add_text(slide, 2, 21.6, 17, 1.3,
             [("Escaneá el código para ver resultados, preguntas frecuentes y una calculadora del Chill Index.",
               19, False, False, BLACK)], name="Texto ES")
    add_text(slide, 2, 23.15, 17, 1.3,
             [("Escaneie o código para ver resultados, perguntas frequentes e uma calculadora do Chill Index.",
               19, False, True, BLACK)], name="Texto PT")
    add_text(slide, 2, 24.8, 17, 0.8, [("alejandra-ramirez-000.github.io/Proyecto_JAI", 16, True, False, INK)],
             name="Dirección")
    rule(slide, 25.9, width=0.75)
    add_text(slide, 2, 26.15, 17, 1.2,
             [("Sistema preditivo agroclimático de intensidade pecuária e risco de mortalidade", 15, True, False, BLACK)],
             name="Título del trabajo")
    add_text(slide, 2, 27.35, 17, 0.8, [("Universidad Tecnológica del Uruguay (UTEC) · 41ª JAI–UFSM", 14, False, False, MUTED)],
             name="Institución")
    out = OUT / "cartel_stand.pptx"
    prs.save(str(out))
    return out


if __name__ == "__main__":
    print(f"Cartel escrito en {build()}")
