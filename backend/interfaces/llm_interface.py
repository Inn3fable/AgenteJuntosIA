from abc import ABC, abstractmethod
from typing import Any

class LLMInterface(ABC):
    """
    Contrato para servicios de modelos de lenguaje.
    """
    @abstractmethod
    def invoke(self, messages: Any) -> Any:
        # Ejecuta una consulta al modelo.
        pass

