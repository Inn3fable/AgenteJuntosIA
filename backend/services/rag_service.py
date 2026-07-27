from backend.config.settings import settings
from backend.repositories.vector_repository import VectorRepository
from backend.services.llm_service import LLMService


class RAGService:
    def __init__(self, vector_repository: VectorRepository, llm_service: LLMService):
        self.vector_repository = vector_repository
        self.llm_service = llm_service

    def retrieve_context(self, question: str):
        """
        Recupera los fragmentos más relevantes usando el TOP_K definido en settings (TOP_K = 8).
        """
        return self.vector_repository.search(question, top_k=settings.TOP_K)

    def generate_answer(self, question: str, context: str) -> str:
        """
        Genera una respuesta completa y explicativa a partir del contexto recuperado.
        """
        prompt = f"""Eres el Asistente Virtual institucional experto en normativas y procedimientos.
Tu objetivo es responder a la consulta del usuario de forma EXHAUSTIVA, COMPLETA y DETALLADA, utilizando ÚNICAMENTE la información del contexto proporcionado.

REGLAS DE RESPUESTA OBLIGATORIAS:
1. NO RESUMAS en una sola frase ni omitas detalles si el contexto contiene explicaciones extensas.
2. Si el concepto consultado incluye características, plataformas electrónicas, entidades involucradas (como RENIEC, gobiernos locales, etc.), frecuencia de actualización, o listas de datos que contiene (nombres, DNI, tipo de seguro, etc.), DEBES INCLUIRLOS TODOS EN TU RESPUESTA.
3. Estructura la respuesta usando viñetas o párrafos claros para facilitar la lectura.
4. Mantén un tono formal, técnico e institucional.
5. Si la información solicitada NO se encuentra expresamente en el contexto, responde estrictamente: "{settings.NO_ANSWER}"

================ CONTEXTO RECUPERADO ================
{context}
=====================================================

Consulta del usuario: {question}

Respuesta detallada:"""

        response = self.llm_service.invoke(prompt)

        # Manejo de la respuesta independientemente de si el LLM retorna un string o un objeto AIMessage
        if hasattr(response, "content"):
            content = response.content
            if isinstance(content, list):
                return "".join(
                    item.get("text", "") if isinstance(item, dict) else str(item)
                    for item in content
                ).strip()
            return str(content).strip()

        return str(response).strip()
