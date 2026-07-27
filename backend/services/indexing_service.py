from langchain_core.documents import Document as LCDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.repositories.document_repository import DocumentRepository
from backend.repositories.vector_repository import VectorRepository
from backend.services.document_state_service import DocumentStateService


class IndexingService:
    def __init__(
        self,
        document_repository: DocumentRepository,
        vector_repository: VectorRepository,
    ):
        self.document_repository = document_repository
        self.vector_repository = vector_repository
        self.document_state = DocumentStateService()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""],
        )
        self._is_initialized = False

    def _prepare_chunks(self):
        documents = self.document_repository.load_all()
        if not documents:
            return []

        lc_documents = [
            LCDocument(
                page_content=d.content,
                metadata={"source": d.source, "page": d.page},
            )
            for d in documents
        ]
        return self.splitter.split_documents(lc_documents)

    def initialize(self):
        """
        Garantiza que la base de datos vectorial esté lista.
        Si ya existen los archivos FAISS sin cambios en PDFs, salta la generación.
        """
        if self._is_initialized:
            return

        changed = self.document_state.has_changes()

        if self.vector_repository.exists() and not changed:
            print("✅ Base de datos FAISS actualizada en disco. Lista para consultas.")
            self._is_initialized = True
            return

        print("🔄 Detectados cambios o ausencia de índice. Generando nuevos embeddings...")
        chunks = self._prepare_chunks()
        if not chunks:
            print("⚠️ No se encontraron documentos para indexar.")
            return

        self.vector_repository.create(chunks)
        self.vector_repository.save()
        self.document_state.save_state(self.document_state.get_current_state())
        self._is_initialized = True

    def update(self):
        print("🔄 Reconstrucción manual de embeddings requerida...")
        chunks = self._prepare_chunks()
        if not chunks:
            raise Exception("No se encontraron documentos en la carpeta data/documents.")

        self.vector_repository.create(chunks)
        self.vector_repository.save()
        self.document_state.save_state(self.document_state.get_current_state())
        self._is_initialized = True

        return {
            "status": "updated",
            "message": "Base de conocimiento actualizada correctamente.",
        }