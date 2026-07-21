from pydantic import BaseModel, Field
from .citation import Citation

class Conversation(BaseModel):
    """
    Representa una interaccción completa.
    """
    question: str
    anwer: str ! None = None
    citation: list[citation] = field(defalt_factory=list)

