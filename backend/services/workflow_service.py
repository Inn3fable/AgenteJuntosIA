
from typing import Dict, Any
from backend.graph.state import AgentState


class WorkflowService:
    """
    Servicio encargado de orquestar la ejecución del grafo compilado de LangGraph
    y de unificar la respuesta en un formato consistente para la capa superior.
    """
    def __init__(self, compiled_graph):
        self.graph = compiled_graph

    def execute(self, question: str) -> Dict[str, Any]:
        # Estado inicial limpio
        initial_state: AgentState = {
            "question": question,
            "pregunta": question,
            "triage": None,
            "decision": None,
            "answer": None,
            "respuesta": None,
            "contexto": [],
            "citations": [],
            "citacion": [],
            "rag_success": False,
            "final_action": None
        }

        # Ejecución del grafo completo
        final_state = self.graph.invoke(initial_state)

        # Extracción segura de la respuesta
        respuesta = (
            final_state.get("answer") or
            final_state.get("respuesta") or
            "No se pudo procesar una respuesta adecuada para su consulta."
        )

        # Extracción segura de las citas
        citacion = (
            final_state.get("citations") if final_state.get("citations") is not None
            else final_state.get("citacion", [])
        )

        return {
            "respuesta": respuesta,
            "citacion": citacion,
            "triaje": final_state.get("triage")
        }