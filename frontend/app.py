"""LexCraft AI — AI-Powered Legal Document Studio.

Streamlit frontend: sidebar workspace with Create, Templates, History and
About pages. Talks to the FastAPI backend (POST /generate) and exports
documents as TXT / DOCX / PDF with branding, as per the project spec.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.brand import APP_NAME, APP_TAGLINE, DOCUMENT_TYPES, FOOTER_NOTICE, logo_path  # noqa: E402
from backend.utils.exporters import format_docx, format_pdf, format_txt  # noqa: E402
from backend.utils.preview import document_stats, format_html_preview  # noqa: E402
from frontend.styles import inject_css  # noqa: E402
from frontend.templates_data import TEMPLATES  # noqa: E402

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(
    page_title=f"{APP_NAME} — {APP_TAGLINE}",
    page_icon=str(logo_path()) if logo_path().exists() else "⚖️",
    layout="wide",
)
inject_css()

# ---------------------------------------------------------------- session state
st.session_state.setdefault("history", [])
st.session_state.setdefault("content", None)
st.session_state.setdefault("model", None)
st.session_state.setdefault("doc_type", None)


def _use_template(template_name: str):
    """on_click callback: prefill Create form and navigate there.
    Runs before widgets are instantiated, so widget-backed keys are safe."""
    tpl = TEMPLATES.get(template_name, {})
    st.session_state["f_type"] = template_name if template_name in DOCUMENT_TYPES else "Custom"
    if template_name not in DOCUMENT_TYPES:
        st.session_state["f_type_custom"] = template_name
    st.session_state["f_parties"] = tpl.get("parties", "")
    st.session_state["f_dates"] = tpl.get("dates", "")
    st.session_state["f_terms"] = tpl.get("terms", "")
    st.session_state["nav"] = "🏠 Create Document"


def _record_history(doc_type, parties, dates, terms, content, model):
    st.session_state["history"].insert(
        0,
        {
            "id": datetime.now().strftime("%H%M%S%f"),
            "doc_type": doc_type,
            "parties": parties,
            "dates": dates,
            "terms": terms,
            "content": content,
            "model": model,
            "at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        },
    )


# ---------------------------------------------------------------- sidebar shell
with st.sidebar:
    logo = logo_path()
    if logo.exists():
        import base64

        b64 = base64.b64encode(logo.read_bytes()).decode()
        st.markdown(
            f"""
            <div class="lx-brandline lx-fade">
              <img src="data:image/png;base64,{b64}" width="46">
              <div>
                <div class="lx-brandname">{APP_NAME}</div>
                <div class="lx-brandsub">{APP_TAGLINE}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f"### ⚖️ {APP_NAME}")

    page = st.radio(
        "Navigate",
        ["🏠 Create Document", "🧩 Templates", "🕘 History", "ℹ️ About"],
        key="nav",
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("AI-generated drafts. Always review with a qualified lawyer.")

# ---------------------------------------------------------------- Create page
if page.startswith("🏠"):
    st.markdown(
        f"""
        <div class="lx-hero lx-fade">
          <span class="lx-tag">AI-Powered Legal Drafting</span>
          <h1>{APP_NAME}</h1>
          <p>Describe your agreement once — get a structured, editable draft
          you can export as TXT, DOCX, or PDF.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown("#### 📝 Draft details")
        document_type = st.selectbox("Document Type", DOCUMENT_TYPES, key="f_type")
        if document_type == "Custom":
            document_type = st.text_input("Custom document type", placeholder="e.g. Internship Agreement", key="f_type_custom")
        parties = st.text_area(
            "Parties Involved",
            placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
            height=110,
            key="f_parties",
        )
        dates = st.text_input("Effective Date", placeholder="April 10, 2026", key="f_dates")
        terms = st.text_area(
            "Terms & Conditions (separate each clause with a semicolon)",
            placeholder="Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice",
            height=140,
            key="f_terms",
        )

        # live chips from terms (micro-interaction)
        chips = [t.strip() for t in (terms or "").split(";") if t.strip()]
        if chips:
            st.markdown(
                "<div style='margin-top:-6px'>"
                + "".join(f"<span class='lx-chip'>{i + 1}. {c[:38]}{'…' if len(c) > 38 else ''}</span>" for i, c in enumerate(chips))
                + "</div>",
                unsafe_allow_html=True,
            )

        generate = st.button("✨ Generate Document", type="primary", use_container_width=True)

        # ---- validation with actionable error states
        missing = []
        if not (document_type or "").strip():
            missing.append("document type")
        if not (parties or "").strip():
            missing.append("parties")
        if not (terms or "").strip():
            missing.append("terms")
        if not (dates or "").strip():
            missing.append("effective date")
        if generate and missing:
            st.error("Please fill in: " + ", ".join(missing) + ".")

        if generate and not missing:
            with st.spinner("Drafting your document with Gemini…"):
                try:
                    r = requests.post(
                        f"{BACKEND_URL}/generate",
                        json={
                            "document_type": document_type,
                            "parties": parties,
                            "terms": terms,
                            "dates": dates,
                        },
                        timeout=90,
                    )
                    if r.ok:
                        data = r.json()
                        st.session_state["content"] = data["content"]
                        st.session_state["model"] = data["model"]
                        st.session_state["doc_type"] = document_type
                        _record_history(document_type, parties, dates, terms, data["content"], data["model"])
                        st.success("Document drafted — preview and export below.")
                    else:
                        try:
                            detail = r.json().get("detail", r.text)
                        except Exception:
                            detail = r.text
                        st.error(f"Generation failed ({r.status_code}): {detail}")
                except requests.RequestException as e:
                    st.error(f"Could not connect to the API at `{BACKEND_URL}`. Is the backend running? ({e})")

    with right:
        st.markdown("#### 📄 Document workspace")
        if st.session_state.get("content"):
            content = st.session_state["content"]
            stats = document_stats(content)

            m1, m2, m3 = st.columns(3)
            m1.metric("Words", stats["words"])
            m2.metric("Sections", stats["sections"])
            m3.metric("Clauses", stats["clauses"])

            preview_html = format_html_preview(content)
            st.markdown(f"<div class='lx-preview'>{preview_html}</div>", unsafe_allow_html=True)

            with st.expander("✏️ Edit document", expanded=False):
                edited = st.text_area("Document text", value=content, height=400, key="editor")
                st.session_state["content"] = edited
                if st.button("Apply edits"):
                    st.rerun()

            st.caption(f"Generated with: `{st.session_state.get('model', 'Gemini')}`")
            dl1, dl2, dl3 = st.columns(3)
            fname = (st.session_state.get("doc_type") or "document").lower().replace(" ", "_")
            with dl1:
                st.download_button("⬇️ TXT", format_txt(content), f"{fname}.txt", "text/plain", use_container_width=True)
            with dl2:
                st.download_button("⬇️ DOCX", format_docx(content, st.session_state.get("doc_type") or "Document"), f"{fname}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
            with dl3:
                st.download_button("⬇️ PDF", format_pdf(content, st.session_state.get("doc_type") or "Document"), f"{fname}.pdf", "application/pdf", use_container_width=True)
        else:
            # meaningful empty state
            st.markdown(
                f"""
                <div class="lx-card" style="text-align:center; padding:44px 24px;">
                  <div style="font-size:2.2rem">🗂️</div>
                  <h3 style="margin:8px 0 4px; white-space:normal">No draft yet</h3>
                  <p class="lx-muted" style="color:#93a1bd; word-break:normal; overflow-wrap:break-word">Fill the draft details on the left and hit
                  <b>Generate</b> — your structured draft with stats,
                  editing and exports will appear here.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ---------------------------------------------------------------- Templates page
elif page.startswith("🧩"):
    st.markdown("## 🧩 Template Gallery")
    st.caption("One click pre-fills the Create form with realistic example data — then tweak and generate.")
    cols = st.columns(3)
    for i, (name, tpl) in enumerate(TEMPLATES.items()):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="lx-tpl">
                  <h4>{tpl['icon']} {name}</h4>
                  <div class="lx-muted">{tpl['blurb']}</div>
                  <div class="lx-muted" style="margin-top:8px"><b>Parties:</b> {tpl['parties']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                f"Use {name}",
                key=f"use_{i}",
                use_container_width=True,
                on_click=_use_template,
                args=(name,),
            ):
                st.rerun()

# ---------------------------------------------------------------- History page
elif page.startswith("🕘"):
    st.markdown("## 🕘 Session History")
    history = st.session_state.get("history", [])
    if not history:
        st.markdown(
            """
            <div class="lx-card" style="text-align:center; padding:40px 24px;">
              <div style="font-size:2.2rem">🕘</div>
              <h3 style="margin:8px 0 4px">Nothing here yet</h3>
              <p style="color:#93a1bd">Documents you generate in this session are
              listed here so you can re-open and re-download them anytime.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for h in history:
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1.4, 1.6])
                with c1:
                    st.markdown(f"**{h['doc_type']}**  \n{h['parties']}")
                with c2:
                    st.caption(f"{h['at']}  \n`{h['model']}`")
                with c3:
                    if st.button("Open", key=f"open_{h['id']}"):
                        st.session_state["content"] = h["content"]
                        st.session_state["model"] = h["model"]
                        st.session_state["doc_type"] = h["doc_type"]
                        st.rerun()
                stats = document_stats(h["content"])
                st.caption(f"{stats['words']} words · {stats['sections']} sections · {stats['clauses']} clauses")

# ---------------------------------------------------------------- About page
else:
    st.markdown("## ℹ️ About")
    st.markdown(
        f"""
        <div class="lx-card lx-fade">
          <h3>⚖️ {APP_NAME} — {APP_TAGLINE}</h3>
          <p style="color:#93a1bd">{APP_NAME} turns a short description of your
          agreement — the parties, the effective date and your key terms — into a
          structured, professional legal draft using Google Gemini. Preview it,
          edit it inline, then export it as TXT, DOCX or PDF with consistent
          branding, a terms table and footers.</p>
          <p style="margin-bottom:0"><b>Architecture:</b> Streamlit UI → FastAPI
          (<code>POST /generate</code>) → Gemini document generator → sanitized
          draft → editable preview → TXT/DOCX/PDF exporters.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("#### Getting started")
    st.markdown(
        """
        1. Start the backend: `uvicorn backend.main:app --reload --port 8000`
        2. Start this app: `streamlit run frontend/app.py`
        3. Add your `GEMINI_API_KEY` to `.env` (see `.env.example`)
        4. Pick a template or fill the form, generate, edit, export.
        """
    )
    st.info("⚠️ " + FOOTER_NOTICE)

st.divider()
st.caption(FOOTER_NOTICE)
