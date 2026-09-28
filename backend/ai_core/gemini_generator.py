import os
from dotenv import load_dotenv

from backend.brand import APP_NAME, DISCLAIMER_TITLE

load_dotenv()

SYSTEM_INSTRUCTION = f"""You are {APP_NAME}, a legal-document drafting assistant.
Draft structured legal information based only on the user's supplied facts.
Do not invent names, dates, amounts, addresses, obligations, or laws.
Use clear formal language, numbered sections, and practical clauses.
Include a short '{DISCLAIMER_TITLE}' stating that the generated text is not a substitute for advice from a qualified lawyer and should be reviewed for the applicable jurisdiction.
Return plain text only; do not use Markdown code fences.
"""

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = os.getenv("GEMINI_MODEL", "gemini-flash-latest").strip()
        self.client = None

    def _get_client(self):
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured. Copy .env.example to .env and add your API key.")
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError("Gemini SDK is missing. Run: pip install -r requirements.txt") from exc
        if self.client is None:
            self.client = genai.Client(api_key=self.api_key)
        return self.client

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        client = self._get_client()
        from google.genai import types
        prompt = f"""Create a professional {document_type}.

PARTIES:
{parties}

EFFECTIVE DATE / DATES:
{dates}

TERMS AND CONDITIONS:
{terms}

Requirements:
- Start with the document title.
- Identify the parties and effective date using only supplied information.
- Organize the agreement into logical numbered sections.
- Include the supplied terms faithfully.
- Add only standard neutral clauses necessary for document structure; use placeholders such as [JURISDICTION] when a fact is missing rather than inventing it.
- End with signature blocks for the relevant parties.
- Add an Important Notice about legal review.
"""
        response = client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,
                max_output_tokens=5000,
            ),
        )
        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text
