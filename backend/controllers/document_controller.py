from backend.services.indexing_service import (IndexingService)
from backend.services.document_service import (DocumentService)

class DocumentController:
    """
    Controlador encargado
    de operaciones documentales.
    """
    def __init__(self, indexing_service: IndexingService, document_service: DocumentService):
        self.indexing_service = (indexing_service)
        self.document_service = (document_service)

    def initialize_database(self):
        return (self.indexing_service.initialize())

    def list_documents(self):
        return (self.document_service.list_documents())

    def upload_document(self, file):
        path = (self.document_service.save_document(file))
        # Actualizar FAISS con nuevos documentos
        self.indexing_service.update()

        return path



