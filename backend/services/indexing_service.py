from backend.repositories.document_repository import DocumentRepository
from backend.repositories.vector_repository import VectorRepository
from backend.services.document_state_service import DocumentStateService
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LCDocument

class IndexingService:
    """
    Servicio encargado de preparar y actualizar la base de conocimiento RAG.
    """
    def __init__( self, document_repository: DocumentRepository, vector_repository: VectorRepository):
        self.document_repository = (document_repository)
        self.vector_repository = (vector_repository)
        self.document_state = (DocumentStateService())
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )

    def initialize(self):
        """
        Inicializa la base vectorial.

        - Si no hay cambios:
              carga FAISS

        - Si hay cambios:
              reconstruye embeddings
        """

        changed = (self.document_state.has_changes())

        if (self.vector_repository.exists() and not changed):
            print("Sin cambios. Cargando FAISS...")
            self.vector_repository.load()
            return
            '''
            return {
                "status": "loaded",
                "message": "Vectorstore cargado"
            }'''

        print("Cambios detectados.")
        print("Regenerando embeddings...")

        documents = self.document_repository.load_all()

        if not documents:
            raise Exception("No existen documentos para indexar")


        #self.vector_repository.create(documents)
        chunks = self.splitter.split_documents(
            [
                LCDocument(
                    page_content=d.content,
                    metadata={
                        "source": d.source,
                        "page": d.page
                    }
                )
                for d in documents
            ]
        )
        print(f"Chunks generados: {len(chunks)}")
        self.vector_repository.create(chunks)
        self.vector_repository.save()
        self.document_state.save_state( self.document_state.get_current_state())
        ''''
        return {
            "status": "updated",
            "message": "Base documental actualizada"
        }'''

    def update(self):
        """
        Fuerza una reconstrucción manual.
        Utilizado cuando se sube un PDF desde el frontend.
        """
        print("Actualización manual..." )

        documents = (self.document_repository.load_all())

        if not documents:
            raise Exception("No existen documentos")

        self.vector_repository.create(documents)
        self.vector_repository.save()
        self.document_state.save_state(self.document_state.get_current_state())

        return {
            "status":"updated",
            "message":"Base documental reconstruida"
        }

