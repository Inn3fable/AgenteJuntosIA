from typing import Dict, Any

class WorkflowService:
    """
    Orquesta el flujo del agente.
    """
    def __init__(self, triage_service, rag_service):
        self.triage_service = triage_service
        self.rag_service = rag_service

    def execute(self,question: str) -> Dict[str, Any]:
        """
        Ejecuta el flujo completo.
        """
        # ==========================
        # TRIAJE
        # ==========================
        triage_result = (self.triage_service.analyze(question))

        decision = (triage_result.decision)
        # ==========================
        # AUTO RESOLVER
        # ==========================
        if decision == "AUTO RESOLVER":
            rag_result = (self.rag_service.ask(question))

            return {
                "respuesta":
                    rag_result.get(
                        "answer",
                        "No lo se!!"
                    ),
                "citacion":
                    rag_result.get(
                        "citations",
                        []
                    ),
                "triaje":
                    triage_result
            }
        # ==========================
        # PEDIR INFORMACIÓN
        # ==========================
        elif decision == "PEDIR INFO":
            campos = (triage_result.missing_fields)
            if campos:
                respuesta = (
                        "Necesito la siguiente información "
                        "para poder ayudarte:\n\n"
                        +
                        "\n".join(
                            [
                                f"- {campo}"
                                for campo in campos
                            ]
                        )
                )
            else:
                respuesta = (
                    "Necesito más información "
                    "sobre tu consulta."
                )
            return {
                "respuesta": respuesta,
                "citacion": [],
                "triaje": triage_result
            }
        # ==========================
        # ABRIR TICKET
        # ==========================
        elif decision == "ABRIR TICKET":
            return {
                "respuesta":
                    (
                        "Se debe abrir un ticket "
                        f"con prioridad {triage_result.urgency}."
                    ),
                "citacion":
                    [],
                "triaje":
                    triage_result
            }
        # ==========================
        # FALLBACK
        # ==========================
        return {
            "respuesta":
                "No pude procesar la solicitud.",
            "citacion":
                [],
            "triaje":
                triage_result
        }

