from abc import ABC, abstractmethod
from typing import List
from backend.models.document import Document

class VectorRepositoryInterface(ABC):
    """
    Contrato para almacenamiento vectorial.
    """
    @abstractmethod
    def create(self, documents: List[Document]):
        # Construye el índice vectorial.
        pass

    @abstractmethod
    def save(self):
        # Persiste el índice.
        pass

    @abstractmethod
    def load(self):
        # Carga un índice existente.
        pass

    @abstractmethod
    def search(self, query: str) -> List[Document]:
        # Busca documentos relevantes.
        pass
