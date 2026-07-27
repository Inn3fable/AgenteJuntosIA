from backend.graph.state import AgentState
from backend.models.citation import Citation
from backend.services.rag_service import RAGService
from backend.services.triage_service import TriageService


class GraphNodes:
    """
    Contiene la lógica de ejecución de los nodos del grafo LangGraph.
    """

    def __init__(self, triage_service: TriageService, rag_service: RAGService):
        self.triage_service = triage_service
        self.rag_service = rag_service

    def triaje_node(self, state: AgentState) -> AgentState:
        """
        Nodo inicial: Evaluación del triaje.
        """
        question = state.get("question") or state.get("pregunta", "")
        triage_result = self.triage_service.evaluate(question)

        return {
            **state,
            "triage": triage_result,
            "decision": getattr(triage_result, "category", "AUTO_RESOLVER")
        }

    # Alias
    triage_node = triaje_node

    def auto_resolver_node(self, state: AgentState) -> AgentState:
        """
        Nodo RAG: Ejecuta la búsqueda vectorial y genera la respuesta detallada.
        """
        question = state.get("question") or state.get("pregunta", "")

        # 1. Recuperar fragmentos del PDF mediante RAGService
        docs = self.rag_service.retrieve_context(question)

        if not docs:
            return {
                **state,
                "answer": "No se encontró información relevante en los documentos indexados.",
                "respuesta": "No se encontró información relevante en los documentos indexados.",
                "contexto": [],
                "citations": [],
                "rag_success": False
            }

        # 2. Construir el contexto formateado con identificadores para el LLM
        formatted_chunks = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Documento")
            page = doc.metadata.get("page", "N/A")
            formatted_chunks.append(
                f"[Fragmento {i} - Fuente: {source} (Pág. {page})]\n{doc.page_content}"
            )

        context_text = "\n\n---\n\n".join(formatted_chunks)

        # 3. Formatear las citas de origen
        citations = []
        for doc in docs:
            source = doc.metadata.get("source", "UOP-AIH-P01-V10.pdf")
            page = doc.metadata.get("page", None)
            citations.append(
                Citation(
                    source=source,
                    page=page + 1 if isinstance(page, int) else page,
                    content=doc.page_content[:200] + "..."
                )
            )

        # 4. Generar la respuesta usando el LLM con el contexto
        answer = self.rag_service.generate_answer(question, context_text)

        return {
            **state,
            "answer": answer,
            "respuesta": answer,
            "contexto": docs,
            "citations": citations,
            "citacion": citations,
            "rag_success": True
        }

    # Alias
    auto_resolver = auto_resolver_node

    def abrir_ticket_node(self, state: AgentState) -> AgentState:
        msg = "Su consulta requiere la apertura de un ticket de atención especializada con el equipo del Programa JUNTOS."
        return {**state, "answer": msg, "respuesta": msg}

    abrir_ticket = abrir_ticket_node

    def pedir_info_node(self, state: AgentState) -> AgentState:
        msg = "Por favor, brinde mayores detalles o especifique el procedimiento sobre el cual desea realizar su consulta."
        return {**state, "answer": msg, "respuesta": msg}

    pedir_info = pedir_info_node