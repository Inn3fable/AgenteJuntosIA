from langchain_core.prompts import ChatPromptTemplate
from backend.models.triage import Triage


class TriageService:
    TRIAGE_PROMPT = """
    Eres un especialista en el triaje del asistente JuntosIA.
    Analiza la consulta del usuario y clasifícala en una de las siguientes opciones:

    - AUTO RESOLVER: Preguntas sobre requisitos, normativas, guías o pasos explicados en manuales/documentos.
    - PEDIR INFO: Preguntas incompletas que requieran datos específicos adicionales del usuario (ej. números de DNI, fechas particulares sin especificar).
    - ABRIR TICKET: Excepciones, reportes de errores de sistema, solicitudes de permisos o aprobación explícita.
    """

    def __init__(self, llm_service):
        self.llm = llm_service.get_model()
        self.structured_llm = self.llm.with_structured_output(Triage)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.TRIAGE_PROMPT),
            ("human", "{message}")
        ])

    def analyze(self, message: str) -> Triage:
        try:
            chain = self.prompt | self.structured_llm
            result = chain.invoke({"message": message})
            return result
        except Exception as error:
            print(f"⚠️ [TriageService] Error procesando triaje: {error}")
            return Triage(
                decision="AUTO RESOLVER",
                urgency="MEDIA",
                missing_fields=[]
            )

    def evaluate(self, message: str) -> Triage:
        """Alias de compatibilidad para evitar AttributeError si se llama evaluate"""
        return self.analyze(message)