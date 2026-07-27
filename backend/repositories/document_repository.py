from pathlib import Path
from backend.config.settings import settings
from backend.loaders.pdf_loader import PDFLoader


class DocumentRepository:
    """
    Repositorio encargado de leer todos los PDF del directorio configurado.
    """

    def __init__(self, pdf_loader: PDFLoader):
        self.pdf_loader = pdf_loader

    def load_all(self):
        documents = []
        documents_path = Path(settings.DOCUMENTS_PATH)

        if not documents_path.exists():
            return documents

        pdf_files = documents_path.glob("*.pdf")

        for pdf in pdf_files:
            pdf_documents = self.pdf_loader.load(pdf)
            documents.extend(pdf_documents)

        return documents