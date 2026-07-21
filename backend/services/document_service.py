from pathlib import Path
from backend.config.settings import settings

class DocumentService:
    """
    Servicio encargado de gestionar archivos PDF de conocimiento.
    """
    def list_documents(self):
        documents_path = Path(settings.DOCUMENTS_PATH)

        if not documents_path.exists():
            return []

        return [pdf.name
                    for pdf in documents_path.glob("*.pdf")
                ]

    def save_document(self, uploaded_file):
        documents_path = Path(settings.DOCUMENTS_PATH)
        documents_path.mkdir(parents=True, exist_ok=True)

        file_path = (documents_path / uploaded_file.name)
        with open(file_path, "wb" ) as file:
            file.write( uploaded_file.getbuffer())

        return file_path

