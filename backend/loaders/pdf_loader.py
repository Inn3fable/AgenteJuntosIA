from pathlib import Path
from uuid import uuid4
from langchain_community.document_loaders import PyMuPDFLoader
from backend.models.document import Document

class PDFLoader:
    """
    Loader encargado de leer archivos PDF
    y convertirlos al modelo interno Documentos.
    """
    def load(self, file_path: Path) -> list[Document]:
        #Carga un PDF y devuelve documentos procesados.
        documents = []
        loader = PyMuPDFLoader(str(file_path))
        pages = loader.load()

        for page in pages:
            document = Document(
                id=str(uuid4()),
                content=page.page_content,
                source=str(file_path),
                page=page.metadata.get(
                                        "page",
                                        None
                                    ),
                metadata=page.metadata
            )
            documents.append(document)

        return documents
