import os
from pathlib import Path
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document as LCDocument

from backend.config.settings import settings
from backend.interfaces.vector_repository_interface import VectorRepositoryInterface


class VectorRepository(VectorRepositoryInterface):
    """
    Repositorio vectorial FAISS ajustado estrictamente a la arquitectura del proyecto.
    """

    def __init__(self, embedding_service):
        self.embedding_service = embedding_service
        self.vectorstore_path = str(settings.VECTORSTORE_PATH)
        self.vectorstore: Optional[FAISS] = None

        # Cargar automáticamente si los archivos ya existen en disco
        if self.exists():
            self.load()

    def _get_embedding_instance(self):
        """Obtiene la instancia real de HuggingFaceEmbeddings mediante Lazy Loading."""
        if hasattr(self.embedding_service, "get_model"):
            return self.embedding_service.get_model()
        elif hasattr(self.embedding_service, "get_embeddings"):
            return self.embedding_service.get_embeddings()
        return self.embedding_service

    def exists(self) -> bool:
        """Verifica si existe el índice FAISS guardado."""
        index_file = Path(self.vectorstore_path) / "index.faiss"
        pkl_file = Path(self.vectorstore_path) / "index.pkl"
        return index_file.exists() and pkl_file.exists()

    def create(self, documents: List[LCDocument]):
        """Crea el vectorstore en memoria."""
        if not documents:
            return
        embeddings = self._get_embedding_instance()
        self.vectorstore = FAISS.from_documents(documents, embeddings)

    def save(self):
        """Guarda físicamente el índice en el disco."""
        if self.vectorstore is not None:
            Path(self.vectorstore_path).mkdir(parents=True, exist_ok=True)
            self.vectorstore.save_local(self.vectorstore_path)

    def load(self):
        """Carga el índice FAISS desde el disco."""
        if self.exists():
            embeddings = self._get_embedding_instance()
            self.vectorstore = FAISS.load_local(
                self.vectorstore_path,
                embeddings,
                allow_dangerous_deserialization=True
            )

    def search(self, query: str, top_k: Optional[int] = None) -> List[LCDocument]:
        """Busca por similitud respetando el parámetro top_k."""
        k = top_k if top_k is not None else settings.TOP_K

        if self.vectorstore is None:
            if self.exists():
                self.load()
            else:
                return []

        return self.vectorstore.similarity_search(query, k=k)


