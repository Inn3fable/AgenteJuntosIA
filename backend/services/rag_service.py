from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import  create_stuff_documents_chain
from backend.config.settings import settings
from backend.models.citation import Citation

class RAGService:
    """
    Servicio principal de recuperación y generación de respuestas.
    """
    def __init__(self, llm_service, vector_repository):
        self.llm = (llm_service.get_model())
        self.vector_repository = (vector_repository)
        self.document_chain = (self._create_document_chain())

    def _create_document_chain(self):
        """
        Construye la cadena RAG.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    Eres el especialista del proceso de actualización del programa Juntos.
                    Responde siempre utilizando la información proporcionada en los documentos.
                    Si la información no existe, responde solamente: No lo se!!
                    Contexto:{context}
                    """
                ),
                (
                    "human",
                    "{input}"
                )
            ]
        )
        return create_stuff_documents_chain(
            self.llm,
            prompt,
            document_variable_name="context"
        )

    def ask(self, question: str ) -> dict:
        """
        Ejecuta una consulta RAG completa.
        """
        documents = (
            self.vector_repository
            .search(question)
        )
        if not documents:
            return {
                "answer":
                settings.NO_ANSWER,
                "citations": [],
                "success": False
            }
        langchain_documents = []

        for document in documents:
            from langchain_core.documents import Document
            langchain_documents.append(
                Document(
                    page_content=document.content,
                    metadata=document.metadata
                )
            )

        answer = (
            self.document_chain.invoke(
                {
                    "input": question,
                    "context":
                    langchain_documents
                }
            )
        )

        citations = (
            self._build_citations(
                documents
            )
        )

        if answer.strip() == settings.NO_ANSWER:
            return {
                "answer":
                settings.NO_ANSWER,
                "citations": [],
                "success": False
            }

        return {
            "answer": answer,
            "citations": citations,
            "success": True
        }

    def _build_citations(self, documents) -> list[Citation]:
        """
        Convierte documentos en citas.
        """
        citations = []
        for document in documents:
            citations.append(
                Citation(
                    source=document.source,
                    page=document.page,
                    content=document.content
                )
            )
        return citations

