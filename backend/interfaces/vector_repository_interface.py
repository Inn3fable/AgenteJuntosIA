from abc import ABC, abstractmethod
from typing import List, Optional
from langchain_core.documents import Document as LCDocument


class VectorRepositoryInterface(ABC):
    """
    Interfaz abstracta para el repositorio vectorial.
    Define el contrato que debe cumplir cualquier vectorstore (FAISS, Chroma, etc.).
    """

    @abstractmethod
    def exists(self) -> bool:
        """Verifica si existe el índice persistido."""
        pass

    @abstractmethod
    def create(self, documents: List[LCDocument]):
        """Crea un nuevo índice vectorial a partir de documentos."""
        pass

    @abstractmethod
    def save(self):
        """Persiste el índice vectorial en almacenamiento."""
        pass

    @abstractmethod
    def load(self):
        """Carga el índice vectorial desde el almacenamiento."""
        pass

    @abstractmethod
    def search(self, query: str, top_k: Optional[int] = None) -> List[LCDocument]:
        """Realiza una búsqueda de similitud sobre el índice."""
        pass