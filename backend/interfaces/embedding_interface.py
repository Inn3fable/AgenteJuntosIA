from abc import ABC, abstractmethod

class EmbeddingInterface(ABC):
    """
    Contrato para cualquier proveedor de embeddings.
    """
    @abstractmethod
    def embed_documents(self, documents):
        pass

    @abstractmethod
    def embed_query(self, query: str):
        pass

    @abstractmethod
    def get_model(self):
        pass
