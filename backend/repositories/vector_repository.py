from pathlib import Path
from langchain_community.vectorstores import FAISS
from backend.config.settings import settings
from backend.models.document import Document
from backend.interfaces.vector_repository_interface import VectorRepositoryInterface
from langchain_core.documents import Document as LCDocument

class VectorRepository(VectorRepositoryInterface):
    """
    Implementación concreta del repositorio vectorial usando FAISS.
    """
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vectorstore = None
        self.retriever = None

    def exists(self) -> bool:
        """
        Verifica si existe un índice FAISS almacenado.
        """
        index_file = (Path(settings.VECTORSTORE_PATH) / "index.faiss")
        return index_file.exists()

    def create(self, documents: list[Document]):
        """
        Crea el índice FAISS desde documentos.
        """
        langchain_documents = []
        for document in documents:
            langchain_documents.append(
                LCDocument(
                    page_content=document.content,
                    metadata={
                        "source": document.source,
                        "page": document.page,
                        **document.metadata
                    }
                )
            )
        self.vectorstore = FAISS.from_documents(
            langchain_documents,
            self.embedding_model
        )
        self._create_retriever()

    def save(self):
        """
        Guarda el índice FAISS.
        """
        if self.vectorstore is None:
            raise Exception("No existe vectorstore para guardar")

        Path(settings.VECTORSTORE_PATH).mkdir(parents=True, exist_ok=True)
        self.vectorstore.save_local(str(settings.VECTORSTORE_PATH))

    def load(self):
        """
        Carga un índice FAISS existente.
        """
        self.vectorstore = FAISS.load_local(
            str(settings.VECTORSTORE_PATH),
            self.embedding_model,
            allow_dangerous_deserialization=True
        )
        self._create_retriever()

    def _create_retriever(self):
        """
        Crea el retriever una sola vez.
        """
        self.retriever = (
            self.vectorstore.as_retriever(
                search_type=
                settings.SEARCH_TYPE,
                search_kwargs={
                    "score_threshold":
                    settings.SCORE_THRESHOLD,
                    "k":
                    settings.TOP_K
                }
            )
        )

    def search(self, query: str) -> list[Document]:
        """
        Busca documentos relacionados.
        """
        if self.retriever is None: raise Exception("Retriever no inicializado")
        results = (self.retriever.invoke(query))
        documents = []
        for result in results:
            documents.append(
                Document(
                    id="",
                    content=result.page_content,
                    source=result.metadata.get(
                        "source",
                        ""
                    ),
                    page=result.metadata.get(
                        "page",
                        None
                    ),
                    metadata=result.metadata
                )
            )
        return documents

