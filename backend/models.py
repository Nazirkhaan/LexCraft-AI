from pydantic import BaseModel, Field

class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=100)
    parties: str = Field(..., min_length=2, max_length=4000)
    terms: str = Field(..., min_length=2, max_length=8000)
    dates: str = Field(..., min_length=2, max_length=500)

class DocumentResponse(BaseModel):
    document_type: str
    content: str
    model: str
