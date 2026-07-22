from typing import Literal, List
from pydantic import BaseModel, Field

class Triage(BaseModel):
    """
    Resultado del análisis inicial del agente.
    """
    decision: Literal[
        "AUTO RESOLVER",
        "PEDIR INFO",
        "ABRIR TICKET"
    ]

    urgency: Literal[
        "BAJA",
        "MEDIA",
        "ALTA"
    ] = "MEDIA"

    missing_fields: List[str] = Field(default_factory=list)