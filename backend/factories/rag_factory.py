from backend.services.embedding_service import EmbeddingService
from backend.services.llm_service import LLMService
from backend.repositories.document_repository import DocumentRepository
from backend.repositories.vector_repository import VectorRepository
from backend.loaders.pdf_loader import PDFLoader
from backend.services.indexing_service import IndexingService
from backend.services.rag_service import RAGService
from backend.services.triage_service import TriageService
from backend.services.workflow_service import WorkflowService
from backend.services.document_service import DocumentService
from backend.controllers.document_controller import DocumentController

class RAGFactory:
    """
    Factory encargada de construir
    toda la aplicación RAG.
    """
    @staticmethod
    def create_application():
        """
        Construye todos los servicios
        de la aplicación.
        """
        # ==========================
        # MODELOS IA
        # ==========================
        embedding_service = (EmbeddingService())
        llm_service = (LLMService())

        # ==========================
        # DOCUMENTOS
        # ==========================
        pdf_loader = (PDFLoader())
        document_repository = (DocumentRepository(pdf_loader))

        # ==========================
        # VECTORSTORE
        # ==========================
        vector_repository = (VectorRepository(embedding_service.get_model()))

        # ==========================
        # INDEXACION
        # ==========================
        indexing_service = (IndexingService(document_repository, vector_repository))
        indexing_service.initialize()

        # ==========================
        # SERVICIO DOCUMENTAL
        # ==========================
        document_service = (DocumentService())
        document_controller = (DocumentController(indexing_service, document_service))

        # ==========================
        # SERVICIO RAG
        # ==========================
        rag_service = (RAGService(llm_service, vector_repository))

        # ==========================
        # SERVICIO TRIAJE
        # ==========================
        triage_service = (TriageService(llm_service))

        # ==========================
        # WORKFLOW
        # ==========================
        workflow_service = (WorkflowService(triage_service, rag_service))

        return {"workflow": workflow_service, "documents": document_controller}




