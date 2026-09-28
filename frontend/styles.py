"""LexCraft AI design system — one CSS layer that restyles every Streamlit
widget (buttons, inputs, cards, tabs, sidebar, scrollbar) with a distinct
deep-ink + indigo/teal visual identity."""

ACCENT = "#6366f1"        # indigo
ACCENT_2 = "#2dd4bf"      # teal
INK = "#0b1020"           # deep ink background
SURFACE = "#121a2e"       # card surface
SURFACE_2 = "#1a2440"     # raised surface
TEXT = "#e7ecf6"
MUTED = "#93a1bd"
BORDER = "#26314e"

FONT_UI = "'Segoe UI', 'Inter', system-ui, sans-serif"
FONT_DOC = "Georgia, 'Times New Roman', serif"

_CSS = f"""
<style>
:root {{
  --lx-accent: {ACCENT};
  --lx-accent2: {ACCENT_2};
  --lx-ink: {INK};
  --lx-surface: {SURFACE};
  --lx-surface2: {SURFACE_2};
  --lx-text: {TEXT};
  --lx-muted: {MUTED};
  --lx-border: {BORDER};
  --lx-radius: 16px;
}}

/* ---------- Global canvas ---------- */
.stApp {{
  background:
    radial-gradient(1200px 600px at 85% -10%, rgba(99,102,241,.14), transparent 60%),
    radial-gradient(900px 500px at -10% 110%, rgba(45,212,191,.10), transparent 55%),
    var(--lx-ink);
  color: var(--lx-text);
  font-family: {FONT_UI};
}}
h1, h2, h3, h4 {{ letter-spacing: -0.015em; }}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, #0d1426 0%, #0b1020 100%);
  border-right: 1px solid var(--lx-border);
}}
section[data-testid="stSidebar"] .stRadio label {{
  background: transparent; border-radius: 12px; padding: 8px 12px;
  transition: background .18s ease, border-color .18s ease;
  border: 1px solid transparent; font-size: .95rem;
}}
section[data-testid="stSidebar"] .stRadio label:hover {{ background: rgba(99,102,241,.10); }}
section[data-testid="stSidebar"] .stRadio label[data-checked="true"] {{
  background: linear-gradient(90deg, rgba(99,102,241,.22), rgba(45,212,191,.12));
  border: 1px solid rgba(99,102,241,.45);
}}

/* ---------- Cards ---------- */
.lx-card {{
  background: linear-gradient(180deg, var(--lx-surface2), var(--lx-surface));
  border: 1px solid var(--lx-border);
  border-radius: var(--lx-radius);
  padding: 22px 24px;
  box-shadow: 0 10px 30px rgba(0,0,0,.35);
  animation: lx-rise .35s ease both;
}}
.lx-hero {{
  text-align: center;
  padding: 26px 18px 18px;
  background: linear-gradient(180deg, rgba(99,102,241,.12), transparent 85%);
  border: 1px solid var(--lx-border);
  border-radius: 20px;
  margin-bottom: 10px;
}}
.lx-hero .lx-tag {{
  display: inline-block; font-size: .78rem; font-weight: 600;
  letter-spacing: .14em; text-transform: uppercase;
  color: var(--lx-accent2); margin-bottom: 6px;
}}
.lx-hero h1 {{
  margin: 0; font-size: 2.3rem;
  background: linear-gradient(90deg, #fff, #b9c4ff 55%, var(--lx-accent2));
  -webkit-background-clip: text; background-clip: text; color: transparent;
}}
.lx-hero p {{ color: var(--lx-muted); margin: 6px 0 0; }}
.lx-brandline {{ display:flex; align-items:center; gap:12px; }}
.lx-brandline img {{ border-radius: 12px; }}
.lx-brandname {{ font-weight: 700; font-size: 1.25rem; line-height: 1.1; }}
.lx-brandsub {{ color: var(--lx-muted); font-size: .82rem; }}

/* ---------- Buttons & inputs ---------- */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {{
  border-radius: 12px; border: 1px solid var(--lx-border);
  background: var(--lx-surface2); color: var(--lx-text);
  font-weight: 600; transition: transform .12s ease, box-shadow .18s ease, border-color .18s ease;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
  transform: translateY(-1px); border-color: rgba(99,102,241,.6);
  box-shadow: 0 6px 18px rgba(99,102,241,.25);
}}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"],
.stDownloadButton > button[kind="primary"] {{
  background: linear-gradient(90deg, var(--lx-accent), #8b5cf6 60%, var(--lx-accent2));
  border: none; color: white;
}}
.stTextInput input, .stTextArea textarea, .stSelectbox > div > div {{
  background: var(--lx-surface) !important; color: var(--lx-text) !important;
  border: 1px solid var(--lx-border) !important; border-radius: 12px !important;
}}
.stTextArea textarea:focus, .stTextInput input:focus {{
  border-color: var(--lx-accent) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,.22) !important;
}}
.stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label, .stCaption {{
  color: var(--lx-muted) !important;
}}
div[data-baseweb="select"] > div {{
  background: var(--lx-surface); border-color: var(--lx-border);
}}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {{ gap: 6px; }}
.stTabs [data-baseweb="tab"] {{
  background: var(--lx-surface); border: 1px solid var(--lx-border);
  border-radius: 12px 12px 0 0; padding: 8px 18px; color: var(--lx-muted);
}}
.stTabs [aria-selected="true"] {{
  background: linear-gradient(90deg, rgba(99,102,241,.25), rgba(45,212,191,.15));
  color: #fff; border-color: rgba(99,102,241,.5);
}}
.stTabs [data-baseweb="tab-highlight"] {{ background: transparent; }}
.stTabs [data-baseweb="tab-border"] {{ display: none; }}

/* ---------- Metrics ---------- */
[data-testid="stMetric"] {{
  background: var(--lx-surface); border: 1px solid var(--lx-border);
  border-radius: 14px; padding: 14px 16px;
}}
[data-testid="stMetricValue"] {{ color: var(--lx-accent2); }}

/* ---------- Document preview ---------- */
.lx-preview {{
  background: #0d1326; border: 1px solid var(--lx-border); border-radius: var(--lx-radius);
  padding: 30px 34px; max-height: 620px; overflow: auto;
  font-family: {FONT_DOC}; line-height: 1.7; color: #e9edf7;
}}
.lx-preview .lx-title {{ text-align:center; font-size:1.15rem; letter-spacing:.06em; margin: 0 0 14px; }}
.lx-preview .lx-heading {{ font-size:1.02rem; margin: 18px 0 6px; color:#cdd7ff; }}
.lx-preview .lx-para {{ margin: 6px 0; }}
.lx-preview .lx-list {{ margin: 4px 0 10px 18px; }}
.lx-preview::-webkit-scrollbar {{ width: 10px; }}
.lx-preview::-webkit-scrollbar-thumb {{ background: var(--lx-surface2); border-radius: 8px; }}
.lx-chip {{
  display:inline-block; padding: 3px 12px; border-radius: 999px; font-size:.78rem;
  border: 1px solid rgba(45,212,191,.4); color: var(--lx-accent2);
  background: rgba(45,212,191,.08); margin-right: 6px;
}}

/* ---------- Template gallery cards ---------- */
.lx-tpl {{
  background: var(--lx-surface); border: 1px solid var(--lx-border);
  border-radius: var(--lx-radius); padding: 16px 18px; height: 100%;
  transition: border-color .18s ease, transform .12s ease;
}}
.lx-tpl:hover {{ border-color: rgba(99,102,241,.55); transform: translateY(-2px); }}
.lx-tpl h4 {{ margin: 0 0 4px; }}
.lx-tpl .lx-muted {{ color: var(--lx-muted); font-size: .84rem; }}

/* ---------- Scrollbar (global) ---------- */
::-webkit-scrollbar {{ width: 10px; height: 10px; }}
::-webkit-scrollbar-thumb {{ background: #232e4c; border-radius: 8px; }}
::-webkit-scrollbar-track {{ background: transparent; }}

/* ---------- Animations ---------- */
@keyframes lx-rise {{
  from {{ opacity: 0; transform: translateY(8px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
.lx-fade {{ animation: lx-rise .4s ease both; }}
hr {{ border-color: var(--lx-border) !important; }}
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(_CSS, unsafe_allow_html=True)
