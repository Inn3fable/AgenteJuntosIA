from langchain_huggingface import HuggingFaceEmbeddings
from backend.config.settings import settings
from backend.interfaces.embedding_interface import EmbeddingInterface

class EmbeddingService(EmbeddingInterface):
    """
    Servicio encargado de generar embeddings.
    """
    def __init__(self):
        self.embedding_model = (
            HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={
                    "device": settings.DEVICE
                },
                encode_kwargs={
                    "normalize_embeddings":
                    settings.NORMALIZE_EMBEDDINGS
                }
            )
        )

    def embed_documents(self, documents):
        """
        Genera embeddings de documentos.
        """
        return self.embedding_model.embed_documents(documents)

    def embed_query(self, query: str):
        """
        Genera embedding de una pregunta.
        """
        return self.embedding_model.embed_query(query)

    def get_model(self):
        """
        Devuelve el modelo compatible
        con LangChain FAISS.
        """
        return self.embedding_model

