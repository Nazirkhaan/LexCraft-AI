"""Document exporters for LexCraft AI.

Converts AI-generated legal draft text into structured .docx, .pdf and .txt
files with branding (logo, serif typography), automatic terms table and
footers, as required by the project specification.
"""

from io import BytesIO

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from fpdf import FPDF

from backend.brand import APP_NAME, EXPORT_FOOTER, logo_path

LOGO = logo_path()


def _lines(text):
    return [x.strip() for x in text.splitlines() if x.strip()]


def extract_terms(text: str):
    """Extract semicolon-separated terms from an 'TERMS AND CONDITIONS' style
    section, falling back to top-level clauses. Used to build the DOCX table."""
    terms = []
    capture = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.upper().startswith("TERMS AND CONDITIONS") or line.upper().startswith("TERMS &"):
            capture = True
            continue
        if capture:
            if line.endswith(";"):
                terms.append(line.rstrip(";").strip())
            elif line and not line[:1].isdigit():
                break
    if not terms:
        for raw in text.splitlines():
            line = raw.strip()
            if ";" in line:
                terms.extend(t.strip() for t in line.split(";") if t.strip())
    return terms


def format_docx(text: str, doc_type: str) -> bytes:
    """Word document: logo, Times New Roman, headings, terms table, footer."""
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)

    if LOGO.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(LOGO), width=Inches(1.2))

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.add_run(doc_type.upper())
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)

    for line in _lines(text):
        is_heading = _is_heading(line)
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(line)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.bold = is_heading

    terms = extract_terms(text)
    if terms:
        doc.add_paragraph()
        ht = doc.add_paragraph()
        hr = ht.add_run("SCHEDULE OF KEY TERMS")
        hr.bold = True
        hr.font.name = "Times New Roman"
        hr.font.size = Pt(12)
        table = doc.add_table(rows=1, cols=3)
        table.style = "Table Grid"
        hdr = table.rows[0].cells
        for i, h in enumerate(("#", "Term", "Detail")):
            para = hdr[i].paragraphs[0]
            run = para.add_run(h)
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
        for idx, term in enumerate(terms, start=1):
            row = table.add_row().cells
            label = term.split(":")[0].strip() if ":" in term else f"Clause {idx}"
            detail = term.split(":", 1)[1].strip() if ":" in term else term
            for j, val in enumerate((str(idx), label, detail)):
                para = row[j].paragraphs[0]
                run = para.add_run(val)
                run.font.name = "Times New Roman"
                run.font.size = Pt(10)

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = footer.add_run(f"{EXPORT_FOOTER}")
    fr.font.size = Pt(8)

    out = BytesIO()
    doc.save(out)
    return out.getvalue()


class _BrandPDF(FPDF):
    """A4 PDF with brand header (logo) and footer on every page."""

    def header(self):
        if self.page_no() > 1 and LOGO.exists():
            try:
                self.image(str(LOGO), x=92, y=10, w=25)
            except Exception:
                pass
        self.set_y(38)
        self.set_font("Times", "B", 15)
        self.cell(0, 8, self._doc_title, align="C")
        self.ln(12)

    def footer(self):
        self.set_y(-14)
        self.set_font("Times", "I", 8)
        self.cell(0, 8, EXPORT_FOOTER, align="C")


def format_pdf(text: str, doc_type: str) -> bytes:
    pdf = _BrandPDF(format="A4")
    pdf._doc_title = doc_type.upper()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    for line in _lines(text):
        clean = line.replace("\u2022", "-")
        pdf.set_font("Times", "B" if _is_heading(clean) else "", 11)
        pdf.multi_cell(0, 6, clean)
        pdf.ln(1)
    return bytes(pdf.output())


def _is_heading(line: str) -> bool:
    head = line[:3].rstrip(".")
    return bool(head.isdigit()) or line.isupper() or line.endswith(":")


def format_txt(text: str) -> bytes:
    return text.encode("utf-8")
