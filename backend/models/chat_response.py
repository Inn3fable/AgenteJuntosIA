from typing import List, Optional
from pydantic import BaseModel, Field
from backend.models.citation import Citation


class ChatResponse(BaseModel):
    """
    Respuesta final que recibe el frontend.
    """
    answer : str
    citations: List[Citation] = Field(default_factory = list)
    success: bool = True

