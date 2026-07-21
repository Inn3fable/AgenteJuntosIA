from backend.models.chat_response import ChatResponse, Citation


class ChatController:
    """
        Controller encargado de comunicar
        Streamlit con la lógica del agente.
    """

    def __init__(self, workflow_service):

    self.workflow_service = workflow_service

    def ask(self, question: str) -> ChatResponse:
        """
        Ejecuta una consulta del usuario.
        """
        result = (
            self.workflow_service
            .execute(
                question
            )
        )

    citations = []

    documents = result.get(
                            "citacion",
                            []
                            )

    for citation in documents:
            # Si viene del RAG como modelo externo
            citations.append(
                Citation(
                    source=getattr(
                                    citation,
                                    "source",
                                    "Desconocido"
                                    ),
                    page=getattr(
                                    citation,
                                    "page",
                                    None
                                    ),

                    content=getattr(
                                    citation,
                                    "content",
                                    ""
                                    )
                        )
            )

    return ChatResponse(
                        answer=result.get(
                                        "respuesta",
                                        "No lo se!!"
                        ),
                        citations=citations,
                        success=True
        )




