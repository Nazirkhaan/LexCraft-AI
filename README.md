# LexCraft AI — AI-Powered Legal Document Studio

LexCraft AI turns a short description of your agreement — the parties, the
effective date and your key terms — into a structured, professional legal draft
using Google Gemini. Preview it, edit it inline, then export it as TXT, DOCX or
PDF with consistent branding, a terms table and page footers.

Built as a from-scratch reimplementation of the "LegalEase" reference project
brief (FastAPI + Gemini + Streamlit), with a distinct design system, a
sidebar workspace, template gallery and session history.

## Features

- **AI drafting** — structured legal documents from document type, parties,
  effective date and semicolon-separated terms (Google Gemini, key stays
  server-side).
- **Template gallery** — one-click realistic prefill for 6 document types.
- **Editable preview** — styled document viewer with word/section/clause
  stats and inline editing.
- **Exports** — TXT, DOCX (Times New Roman, terms table, footer) and PDF
  (branded header/footer on every page).
- **Session history** — re-open and re-download anything you generated.
- **Responsive dark UI** — deep-ink + indigo/teal design system, custom
  components, empty states, validation and micro-interactions.

## Project structure

```text
LegalEaseAI/
├── backend/
│   ├── ai_core/gemini_generator.py   # Gemini integration (ai core)
│   ├── utils/exporters.py            # DOCX / PDF / TXT exporters
│   ├── utils/preview.py              # format_html_preview + stats
│   ├── utils/sanitize.py             # text sanitization
│   ├── brand.py                      # brand config (name, tagline, logo)
│   ├── main.py                       # FastAPI app, / and /health
│   ├── models.py                     # DocumentRequest / DocumentResponse
│   └── routes.py                     # POST /generate
├── frontend/
│   ├── app.py                        # Streamlit workspace (4 pages)
│   ├── styles.py                     # LexCraft design system (CSS)
│   └── templates_data.py             # template gallery data
├── assets/lexcraft_logo.png          # brand logo
├── .streamlit/config.toml            # Streamlit theme
├── tests/                            # pytest suite
├── .env.example
└── requirements.txt
```

## Quick start

### 1. Create a virtual environment

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install packages

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini

Copy `.env.example` to `.env` and add your Google Gemini API key:

```env
GEMINI_API_KEY=your_real_key
GEMINI_MODEL=gemini-flash-latest
BACKEND_URL=http://127.0.0.1:8000
```

Never commit `.env`.

### 4. Start the backend

```bash
uvicorn backend.main:app --reload --port 8000
```

Check http://127.0.0.1:8000/health — it should return `{"status": "ok"}`.

### 5. Start the frontend

```bash
streamlit run frontend/app.py
```

Open http://localhost:8501.

### 6. Run the tests

```bash
pytest -q
```

## Workflow

```text
Streamlit UI (Create / Templates / History / About)
    │ POST /generate {document_type, parties, terms, dates}
    ▼
FastAPI  ── DocumentRequest (Pydantic validation)
    ▼
GeminiDocumentGenerator  ── structured prompt + system instruction
    ▼
Google Gemini API
    ▼
Sanitized draft
    ├── Editable styled preview (+ word/section/clause stats)
    ├── TXT exporter
    ├── DOCX exporter (logo, Times New Roman, terms table, footer)
    └── PDF exporter (branded header/footer on every page)
```

## API

| Method | Path      | Purpose                                   |
|--------|-----------|-------------------------------------------|
| GET    | `/`       | Service banner                            |
| GET    | `/health` | Health check                              |
| POST   | `/generate` | Generate a draft from form fields       |
| GET    | `/docs`   | Interactive OpenAPI docs                  |

## Configuration

| Variable        | Default                | Purpose                     |
|-----------------|------------------------|-----------------------------|
| `GEMINI_API_KEY`| — (required)           | Google Gemini API key       |
| `GEMINI_MODEL`  | `gemini-flash-latest`  | Preferred model; the backend auto-retries and falls back through stable aliases on Google-side availability errors |
| `BACKEND_URL`   | `http://127.0.0.1:8000`| Backend URL used by the UI  |

## Deployment (one public URL)

The repo ships a single-container OCI setup (`Containerfile`, built with
Podman) that runs **nginx + Streamlit + FastAPI** behind **one public port**
(`$PORT`, default 8080):

- `/` → Streamlit UI (WebSocket-proxied)
- `/health` → FastAPI health endpoint
- `/api/…` → FastAPI (same-origin API, e.g. `POST /api/generate`)

Local test with Podman:

```bash
podman build -t lexcraft .
podman run --rm -p 8080:8080 --env-file .env lexcraft
# open http://localhost:8080
```

Hosted deployment (Render free tier): connect the repo and use the committed
`render.yaml` Blueprint, or create a Docker web service with health check
`/health`. Set `GEMINI_API_KEY` in the hosting dashboard only — it is never
committed. See `deploy/` for the proxy and process-manager configuration.

## Scope note

LexCraft AI generates legal-document drafts from user-provided information.
It does not establish that a document is legally valid for a particular
jurisdiction. Review generated documents with a qualified legal professional
before relying on them.

## Credits

Built on the workflow described in the public "LegalEase" project brief
(Streamlit + FastAPI + Gemini document generator). All UI, branding, and
export enhancements in this repository are original work.
