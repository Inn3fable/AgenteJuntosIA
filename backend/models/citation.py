from pydantic import BaseModel, Field

class Citation(BaseModel):
    ""

    source: str = Field(description = "Archivo origen")
    page: int | None = Field(default = None)
    content: str = Field(description="Fragmento utilizado como evidencia")
