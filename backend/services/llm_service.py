from langchain_google_genai import  ChatGoogleGenerativeAI
from backend.config.settings import settings
from backend.interfaces.llm_interface import LLMInterface

class LLMService(LLMInterface):
    """
    Servicio encargado del modelo de lenguaje.
    """
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            temperature=settings.TEMPERATURE,
            google_api_key=settings.GEMINI_API_KEY

        )

    def invoke( self, messages):
        return self.llm.invoke(
            messages
        )

    def get_model(self):
        return self.llm

