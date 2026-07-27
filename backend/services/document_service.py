from pathlib import Path
from backend.config.settings import settings

class DocumentService:
    def __init__(self):
        self.documents_dir = Path(settings.DOCUMENTS_PATH)
        self.documents_dir.mkdir(parents=True, exist_ok=True)

    def list_documents(self) -> list[str]:
        if not self.documents_dir.exists():
            return []
        return [f.name for f in self.documents_dir.glob("*.pdf")]

    def save_document(self, file) -> Path:
        file_path = self.documents_dir / file.name
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        return file_path