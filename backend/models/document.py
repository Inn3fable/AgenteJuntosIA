from pydantic import BaseModel, Field
from typing import Dist


class Document(BaseModel):
    """
    Representa un documento procesado dentro del sistema RAG.
    """
    id: str = Field(description="Identificador único del documento")
    content: str = Field(description="Contenido textual del documento")
    source: str = Field(description="Ruta u origen del documento")
    page: int | None = Field(default=None, description="Número de página del documento")
    metadata: Dict = Field(default_factory=dict, description="Metadatos adicionales")


