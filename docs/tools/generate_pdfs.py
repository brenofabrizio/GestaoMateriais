from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "pdf"

DOCUMENTS = {
    "TRD-Gestao-de-Materiais.pdf": ("TRD — Arquitetura Técnica", ROOT / "docs" / "TRD.md"),
    "App-Flow-Gestao-de-Materiais.pdf": ("App Flow — Gestão de Materiais", ROOT / "docs" / "APP-FLOW.md"),
    "UI-UX-Design-Gestao-de-Materiais.pdf": ("UI/UX Design — Gestão de Materiais", ROOT / "docs" / "UI-UX-DESIGN.md"),
    "Plano-Implementacao-Gestao-de-Materiais.pdf": ("Plano de Implementação — Gestão de Materiais", ROOT / "docs" / "IMPLEMENTATION-PLAN.md"),
    "Arquitetura-Inicial-Gestao-de-Materiais.pdf": ("Arquitetura Inicial — Gestão de Materiais", ROOT / "docs" / "arquitetura-inicial.md"),
}

FOREST = colors.HexColor("#123b35")
FOREST_LIGHT = colors.HexColor("#e7f3e6")
LIME = colors.HexColor("#c8f36c")
TEXT = colors.HexColor("#17221f")
MUTED = colors.HexColor("#60746a")
BORDER = colors.HexColor("#dce7df")


def register_fonts():
    candidates = [
        ("DejaVu", "C:/Windows/Fonts/arial.ttf", "DejaVu-Bold", "C:/Windows/Fonts/arialbd.ttf"),
        ("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ]
    for regular_name, regular_path, bold_name, bold_path in candidates:
        if Path(regular_path).exists() and Path(bold_path).exists():
            pdfmetrics.registerFont(TTFont(regular_name, regular_path))
            pdfmetrics.registerFont(TTFont(bold_name, bold_path))
            return regular_name, bold_name
    return "Helvetica", "Helvetica-Bold"


REGULAR, BOLD = register_fonts()


def inline_markup(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", rf'<font name="{REGULAR}"><b>\1</b></font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def styles():
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName=REGULAR, fontSize=9.5, leading=14, textColor=TEXT, spaceAfter=7),
        "h1": ParagraphStyle("H1", parent=base["Heading1"], fontName=BOLD, fontSize=23, leading=28, textColor=FOREST, spaceBefore=10, spaceAfter=13),
        "h2": ParagraphStyle("H2", parent=base["Heading2"], fontName=BOLD, fontSize=15, leading=19, textColor=FOREST, spaceBefore=15, spaceAfter=8),
        "h3": ParagraphStyle("H3", parent=base["Heading3"], fontName=BOLD, fontSize=11, leading=14, textColor=TEXT, spaceBefore=10, spaceAfter=5),
        "bullet": ParagraphStyle("Bullet", parent=base["BodyText"], fontName=REGULAR, fontSize=9.5, leading=14, leftIndent=13, firstLineIndent=-8, textColor=TEXT, spaceAfter=3),
        "small": ParagraphStyle("Small", parent=base["BodyText"], fontName=REGULAR, fontSize=8, leading=11, textColor=MUTED),
        "cover_title": ParagraphStyle("CoverTitle", parent=base["Title"], fontName=BOLD, fontSize=30, leading=36, textColor=colors.white, alignment=TA_CENTER),
        "cover_subtitle": ParagraphStyle("CoverSubtitle", parent=base["BodyText"], fontName=REGULAR, fontSize=12, leading=18, textColor=colors.HexColor("#d5e9df"), alignment=TA_CENTER),
        "code": ParagraphStyle("Code", parent=base["Code"], fontName="Courier", fontSize=7.5, leading=10, textColor=colors.HexColor("#dcefe5")),
    }


class PDFDocument(BaseDocTemplate):
    def __init__(self, filename, title, **kwargs):
        super().__init__(filename, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=20 * mm, bottomMargin=16 * mm, **kwargs)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=self.draw_page)])
        self.title = title

    def draw_page(self, canvas, doc):
        canvas.saveState()
        width, height = A4
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.5)
        canvas.line(self.leftMargin, height - 13 * mm, width - self.rightMargin, height - 13 * mm)
        canvas.setFont(REGULAR, 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(self.leftMargin, height - 10 * mm, "GESTÃO DE MATERIAIS")
        canvas.drawRightString(width - self.rightMargin, height - 10 * mm, self.title)
        canvas.line(self.leftMargin, 11 * mm, width - self.rightMargin, 11 * mm)
        canvas.drawString(self.leftMargin, 7 * mm, "Documento técnico — versão inicial")
        canvas.drawRightString(width - self.rightMargin, 7 * mm, f"Página {doc.page}")
        canvas.restoreState()


def is_table_start(lines, index):
    return index + 1 < len(lines) and lines[index].strip().startswith("|") and re.match(r"^\s*\|?\s*:?-{3,}", lines[index + 1])


def table_rows(lines, index):
    rows = []
    while index < len(lines) and lines[index].strip().startswith("|"):
        raw = lines[index].strip().strip("|")
        if re.match(r"^\s*:?-{3,}", raw):
            index += 1
            continue
        rows.append([inline_markup(cell.strip()) for cell in raw.split("|")])
        index += 1
    return rows, index


def parse_markdown(path, styles_map):
    lines = path.read_text(encoding="utf-8").splitlines()
    flow = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            language = line[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            flow.append(("code", "\n".join(code), language))
            continue
        match = re.match(r"^(#{1,3})\s+(.*)$", line)
        if match:
            level = len(match.group(1))
            flow.append((f"h{level}", inline_markup(match.group(2))))
            i += 1
            continue
        if is_table_start(lines, i):
            rows, i = table_rows(lines, i)
            flow.append(("table", rows))
            continue
        if re.match(r"^[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].strip()))
                i += 1
            flow.append(("bullets", items))
            continue
        if re.match(r"^\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            flow.append(("numbered", items))
            continue
        paragraph = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,3})\s+|^```|^[-*]\s+|^\d+\.\s+|^\s*\|", lines[i]):
            paragraph.append(lines[i].strip())
            i += 1
        flow.append(("paragraph", " ".join(paragraph)))
    return flow


def make_story(title, source):
    s = styles()
    story = []
    story.append(Spacer(1, 35 * mm))
    cover_data = [[Paragraph(inline_markup(title), s["cover_title"])], [Spacer(1, 10 * mm)], [Paragraph("Gestão de Materiais Corporativo", s["cover_subtitle"])], [Spacer(1, 5 * mm)], [Paragraph(datetime.now().strftime("Gerado em %d/%m/%Y"), s["cover_subtitle"])]]
    cover = Table(cover_data, colWidths=[150 * mm], rowHeights=[None, None, None, None, None])
    cover.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), FOREST), ("BOX", (0, 0), (-1, -1), 0, FOREST), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 22), ("RIGHTPADDING", (0, 0), (-1, -1), 22), ("TOPPADDING", (0, 0), (-1, -1), 24), ("BOTTOMPADDING", (0, 0), (-1, -1), 24)]))
    story.append(cover)
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph(f"Fonte: {source.name}", s["small"]))
    story.append(PageBreak())

    flow = parse_markdown(source, s)
    for kind, value, *extra in flow:
        if kind == "h1":
            continue
        if kind == "h2":
            story.append(Paragraph(value, s["h2"]))
        elif kind == "h3":
            story.append(Paragraph(value, s["h3"]))
        elif kind == "paragraph":
            story.append(Paragraph(inline_markup(value), s["body"]))
        elif kind == "bullets":
            for item in value:
                story.append(Paragraph(f"• {inline_markup(item)}", s["bullet"]))
            story.append(Spacer(1, 3))
        elif kind == "numbered":
            for position, item in enumerate(value, 1):
                story.append(Paragraph(f"{position}. {inline_markup(item)}", s["bullet"]))
            story.append(Spacer(1, 3))
        elif kind == "table":
            data = [[Paragraph(cell, s["small"]) for cell in row] for row in value]
            col_count = max(len(row) for row in data)
            widths = [((A4[0] - 36 * mm) / col_count) for _ in range(col_count)]
            table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), FOREST),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), BOLD),
                ("GRID", (0, 0), (-1, -1), 0.35, BORDER),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, FOREST_LIGHT]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(Spacer(1, 4))
            story.append(table)
            story.append(Spacer(1, 8))
        elif kind == "code":
            language = extra[0] if extra else ""
            if language == "mermaid":
                story.append(Paragraph("Fluxo visual", s["h3"]))
            story.append(Preformatted(value, s["code"], maxLineLength=115))
            story.append(Spacer(1, 7))
    return story


def generate():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, (title, source) in DOCUMENTS.items():
        destination = OUT / filename
        document = PDFDocument(str(destination), title, author="Hermes Agent")
        document.build(make_story(title, source))
        print(destination)


if __name__ == "__main__":
    generate()
