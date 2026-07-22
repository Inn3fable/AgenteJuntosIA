from pydantic import BaseModel, Field
from .citation import Citation

class Conversation(BaseModel):
    """
    Representa una interaccción completa.
    """
    question: str
    answer: str | None = None
    citation: list[Citation] = Field(default_factory=list)

