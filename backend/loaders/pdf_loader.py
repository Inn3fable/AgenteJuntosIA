from pathlib import Path
from uuid import uuid4
from langchain_community.document_loaders import PyMuPDFLoader
from backend.models.document import Document


class PDFLoader:
    """
    Carga archivos PDF de forma rápida y los transforma en el modelo interno Document.
    """

    def load(self, file_path: Path) -> list[Document]:
        file_path_obj = Path(file_path) if isinstance(file_path, str) else file_path

        if not file_path_obj.exists():
            raise FileNotFoundError(f"No se encontró el archivo en la ruta: {file_path_obj}")

        # PyMuPDFLoader extrae todas las páginas rápidamente
        loader = PyMuPDFLoader(str(file_path_obj))
        pages = loader.load()

        documents = []
        for idx, page in enumerate(pages):
            content = page.page_content.strip() if page.page_content else ""
            if not content:
                continue

            # Ajuste de página base 1
            raw_page = page.metadata.get("page", idx)
            page_num = (raw_page + 1) if isinstance(raw_page, int) else (idx + 1)

            # Preservar metadatos
            meta = dict(page.metadata) if page.metadata else {}
            meta.update({
                "source": file_path_obj.name,
                "page": page_num,
                "total_pages": len(pages)
            })

            documents.append(
                Document(
                    id=str(uuid4()),
                    content=content,
                    source=file_path_obj.name,
                    page=page_num,
                    metadata=meta
                )
            )

        return documents