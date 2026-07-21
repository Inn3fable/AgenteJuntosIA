from typing import List, Optional
from pydantic import BaseModel, field

class Citation(BaseModel):
    """
    Información del docuemto usado por el RAG.
    """
    source : str
    page: Opctional[int] = None
    Content: str

class ChatResponse(BaseModel):
    """
    Respuesta final que recibe el frontend.
    """
    answer : str
    citations: List[Citation] = Field(default_factory = list)
    success: bool = True

