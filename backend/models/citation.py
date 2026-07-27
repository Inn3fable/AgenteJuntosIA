from typing import Optional
from pydantic import BaseModel, ConfigDict


class Citation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source: str
    page: Optional[int] = None
    content: str