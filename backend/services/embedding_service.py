from langchain_huggingface import HuggingFaceEmbeddings
from backend.config.settings import settings
from backend.interfaces.embedding_interface import EmbeddingInterface


class EmbeddingService(EmbeddingInterface):
    """
    Servicio de embeddings con carga perezosa (Lazy Loading).
    Evita bloquear el arranque inicial de Streamlit.
    """
    def __init__(self):
        self._embedding_model = None

    def get_model(self):
        """Inicializa e instancia HuggingFaceEmbeddings solo bajo demanda."""
        if self._embedding_model is None:
            print("⚡ [EmbeddingService] Cargando modelo BAAI/bge-m3 en RAM...")
            self._embedding_model = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={"device": settings.DEVICE},
                encode_kwargs={"normalize_embeddings": settings.NORMALIZE_EMBEDDINGS},
            )
        return self._embedding_model

    def get_embeddings(self):
        """Alias para obtener la instancia del modelo para FAISS."""
        return self.get_model()

    def embed_documents(self, documents):
        return self.get_model().embed_documents(documents)

    def embed_query(self, query: str):
        return self.get_model().embed_query(query)