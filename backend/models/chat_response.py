from typing import List
from pydantic import BaseModel, ConfigDict
from backend.models.citation import Citation

class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    answer: str
    citations: List[Citation] = []
    success: bool = True