from typing import TypedDict, Optional, List

from backend.models.triage import Triage
from backend.models.citation import Citation


class AgentState(TypedDict, total=False):
    """
    Estado global del agente LangGraph.

    Este objeto viaja entre todos los nodos:

    TRIAJE
        |
        |
    AUTO_RESOLVER
        |
        |
    PEDIR_INFO / ABRIR_TICKET / END

    """

    # Pregunta original del usuario
    question: str

    # Resultado del análisis inicial
    # generado por TriageService
    triage: Optional[Triage]

    # Respuesta final del agente
    answer: Optional[str]

    # Documentos usados por RAG
    citations: List[Citation]

    # Indica si RAG encontró respuesta válida
    rag_success: bool

    # Acción final tomada
    final_action: Optional[str]