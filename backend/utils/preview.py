"""Shared UI utilities for the LexCraft AI frontend."""

import html
import re


def format_html_preview(text: str) -> str:
    """Convert generated draft text into a semantic, stylized HTML preview
    (titles, numbered section headings, bullets, paragraphs) as required by
    the project specification. Output is escaped — safe to embed."""
    lines = [ln.rstrip() for ln in (text or "").splitlines()]
    out = []
    in_list = False
    for ln in lines:
        s = ln.strip()
        if not s:
            if in_list:
                out.append("</ul>")
                in_list = False
            continue
        esc = html.escape(s)
        if _is_title(s):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f'<h1 class="lx-title">{esc}</h1>')
        elif _is_heading(s):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f'<h2 class="lx-heading">{esc}</h2>')
        elif s.startswith(("-", "\u2022", "*")):
            if not in_list:
                out.append('<ul class="lx-list">')
                in_list = True
            out.append(f"<li>{esc.lstrip('-\u2022* ').strip()}</li>")
        else:
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f'<p class="lx-para">{esc}</p>')
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def _is_heading(line: str) -> bool:
    head = line[:3].rstrip(".")
    return bool(head.isdigit()) or (line.isupper() and len(line) > 3) or line.endswith(":")


def _is_title(line: str) -> bool:
    words = line.split()
    return len(words) <= 10 and line.isupper() and not line.endswith(":")


def document_stats(text: str) -> dict:
    """Small stats used by the preview toolbar: words, sections, clauses."""
    lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]
    words = len(re.findall(r"\S+", text or ""))
    sections = sum(1 for ln in lines if re.match(r"^\d+\s*[\.\)]?\s+\S", ln))
    clauses = sum(1 for ln in lines if ln.endswith(";"))
    return {"words": words, "sections": sections, "clauses": clauses}
