from backend.utils.exporters import extract_terms, format_docx, format_pdf, format_txt
from backend.utils.preview import document_stats, format_html_preview

SAMPLE = (
    "CONSULTING AGREEMENT\n"
    "\n"
    "This Agreement is made between Alice Smith (Consultant) and Acme Corp (Client).\n"
    "\n"
    "TERMS AND CONDITIONS:\n"
    "1. Payment: Within 30 days of invoice;\n"
    "2. Confidentiality: Maintained at all times;\n"
    "3. Termination: 15 days notice;\n"
    "\n"
    "Important Notice: Review before use."
)

def test_exports():
    text = "LEGAL AGREEMENT\n\n1. Payment: Within 30 days.\n\nImportant Notice: Review before use."
    assert format_txt(text).startswith(b"LEGAL")
    assert format_docx(text, "Agreement").startswith(b"PK")
    assert format_pdf(text, "Agreement").startswith(b"%PDF")

def test_docx_terms_table():
    data = format_docx(SAMPLE, "Consulting Agreement")
    assert data.startswith(b"PK") and len(data) > 5000

def test_pdf_multiline():
    data = format_pdf(SAMPLE, "Consulting Agreement")
    assert data.startswith(b"%PDF")

def test_extract_terms():
    terms = extract_terms(SAMPLE)
    assert len(terms) == 3 and "Payment" in terms[0]

def test_html_preview():
    html = format_html_preview(SAMPLE)
    assert "lx-title" in html and "CONSULTING AGREEMENT" in html
    assert "lx-heading" in html and "&lt;" not in html.replace("&lt;b&gt;", "")

def test_document_stats():
    stats = document_stats(SAMPLE)
    assert stats["words"] > 20 and stats["sections"] >= 3 and stats["clauses"] == 3
