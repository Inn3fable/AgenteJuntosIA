from backend.controllers.chat_controller import ChatController
from backend.controllers.document_controller import DocumentController
from backend.graph.nodes import GraphNodes
from backend.graph.workflow import build_workflow
from backend.repositories.vector_repository import VectorRepository
from backend.services.embedding_service import EmbeddingService
from backend.services.llm_service import LLMService
from backend.services.rag_service import RAGService
from backend.services.triage_service import TriageService
from backend.services.workflow_service import WorkflowService


class RAGFactory:
    @staticmethod
    def create_application() -> dict:
        """
        Ensambla todas las dependencias del backend (LLM, Embeddings, VectorStore, Nodos, Grafo)
        y retorna los controladores listos para ser consumidos por el Frontend (Streamlit).
        """
        # 1. Servicios base e infraestructura
        llm_service = LLMService()
        embedding_service = EmbeddingService()
        vector_repository = VectorRepository(embedding_service=embedding_service)

        # 2. Cargar índice vectorial si existe
        if vector_repository.exists():
            vector_repository.load()

        # 3. Servicios de negocio
        rag_service = RAGService(
            vector_repository=vector_repository,
            llm_service=llm_service
        )
        triage_service = TriageService(llm_service=llm_service)

        # 4. Nodos de LangGraph con sus dependencias
        graph_nodes = GraphNodes(
            triage_service=triage_service,
            rag_service=rag_service
        )

        # 5. Compilar el flujo
        compiled_graph = build_workflow(graph_nodes)

        # 6. Servicio de orquestación
        workflow_service = WorkflowService(compiled_graph=compiled_graph)

        # 7. Controladores
        chat_controller = ChatController(workflow_service=workflow_service)
        document_controller = DocumentController(
            rag_service=rag_service,
            vector_repository=vector_repository
        )

        return {
            "chat_controller": chat_controller,
            "document_controller": document_controller,
            "workflow_service": workflow_service,
            "rag_service": rag_service
        }