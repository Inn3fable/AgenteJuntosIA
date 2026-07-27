from typing import TypedDict, List, Optional, Any
from backend.models.triage import Triage
from backend.models.citation import Citation


class AgentState(TypedDict, total=False):
    question: Optional[str]
    pregunta: Optional[str]
    triage: Optional[Triage]
    decision: Optional[str]
    answer: Optional[str]
    respuesta: Optional[str]
    contexto: Optional[List[Any]]
    citations: Optional[List[Citation]]
    citacion: Optional[List[Citation]]
    rag_success: Optional[bool]
    final_action: Optional[str]