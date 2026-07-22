from pydantic import BaseModel, Field
from .triage import Triage
from .citation import Citation

class AgentState(BaseModel):
    """
    Estado interno del agente LangGraph
    """
    question: str
    triage: Triage | None = None
    answer: str | None = None
    citations: list[Citation] =  Field(default_factory = list)
    rag_success: bool =  False
    final_action: str | None = None

