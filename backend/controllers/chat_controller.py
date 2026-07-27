from backend.models.chat_response import ChatResponse
from backend.services.workflow_service import WorkflowService


class ChatController:
    def __init__(self, workflow_service: WorkflowService):
        self.workflow_service = workflow_service

    def ask(self, prompt: str) -> ChatResponse:
        result = self.workflow_service.execute(prompt)

        raw_answer = result.get("answer") or result.get("respuesta", "")
        raw_triage = result.get("triage")
        formatted_citations = result.get("citations") or result.get("citacion", [])

        # Extraer texto plano si raw_answer es un objeto AIMessage o similar de LangChain
        if hasattr(raw_answer, "content"):
            content = raw_answer.content
            if isinstance(content, list):
                clean_answer = "".join(
                    item.get("text", "") if isinstance(item, dict) else str(item)
                    for item in content
                )
            else:
                clean_answer = str(content)
        else:
            clean_answer = str(raw_answer)

        return ChatResponse(
            answer=clean_answer,
            citations=formatted_citations,
            triage=raw_triage
        )