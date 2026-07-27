from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict

class Document(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    content: str
    source: str
    page: Optional[int] = None
    metadata: Dict[str, Any] = {}