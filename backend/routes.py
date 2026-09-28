from fastapi import APIRouter, HTTPException
from .models import DocumentRequest, DocumentResponse
from .ai_core.gemini_generator import GeminiDocumentGenerator
from .utils.sanitize import sanitize_text

router = APIRouter()
generator = GeminiDocumentGenerator()

@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    try:
        content = generator.generate_document(request.document_type, request.parties, request.terms, request.dates)
        return DocumentResponse(document_type=request.document_type, content=sanitize_text(content), model=generator.model)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
