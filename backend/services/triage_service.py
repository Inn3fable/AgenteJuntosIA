from backend.models.triage import Triage


class TriageService:
    """
    Servicio encargado del análisis inicial de las preguntas del usuario.
    """
    TRIAGE_PROMPT = """
                    Eres un especialista en el triaje del asistente JuntosIA.
                    Analiza el mensaje del usuario y determina la acción correcta.
                    Debes devolver únicamente un JSON con esta estructura:
                    {
                        "decision": "AUTO RESOLVER" | "PEDIR INFO" | "ABRIR TICKET",
                        "urgency": "BAJA" | "MEDIA" | "ALTA", "missing_fields":[]
                    }
                    Reglas:
                        AUTO RESOLVER: Preguntas claras sobre procedimientos, reglas o información existente en los documentos.
                        PEDIR INFO: Cuando la pregunta no tiene suficiente contexto o faltan datos.
                        ABRIR TICKET: Solicitudes de excepción, aprobación, autorización, acceso especial o solicitudes explícitas de ticket.
                    Analiza el siguiente mensaje:
                    """
    def __init__(self,llm_service):
        self.llm = (llm_service.get_model())
        self.structured_llm = ( self.llm.with_structured_output(Triage))

    def analyze(self, message: str) -> Triage:
        """
        Analiza una pregunta y devuelve la clasificación.
        """
        try:
            result = (
                self.structured_llm.invoke(
                    [
                        (
                            "system", self.TRIAGE_PROMPT
                        ),
                        (
                            "human", message
                        )
                    ]
                )
            )
            return result

        except Exception as error:
            print(f"Error en triaje: {error}")
            return Triage(
                decision="ABRIR TICKET",
                urgency="MEDIA",
                missing_fields=[]
            )

