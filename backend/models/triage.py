from pydantic import BaseModel, Field
from typing import List, Literal


class Triage(BaseModel):
    decision: Literal["AUTO RESOLVER", "PEDIR INFO", "ABRIR TICKET"] = Field(
        description="Clasificación de la intención de la consulta"
    )
    urgency: str = Field(default="MEDIA", description="Nivel de urgencia")
    missing_fields: List[str] = Field(
        default_factory=list,
        description="Campos o información adicional faltante"
    )