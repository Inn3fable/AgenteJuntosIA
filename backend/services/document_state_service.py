import json
from pathlib import Path
from backend.config.settings import settings

class DocumentStateService:
    """
    Controla cambios realizados en los documentos PDF.
    """
    def __init__(self):
        self.state_file = ( Path(settings.VECTORSTORE_PATH) / "document_state.json" )

    def get_current_state(self):
        documents_path = Path(settings.DOCUMENTS_PATH)
        state = {}

        if not documents_path.exists():
            return state

        for pdf in documents_path.glob("*.pdf"):
            state[pdf.name] = {
                "size": pdf.stat().st_size,
                "modified": pdf.stat().st_mtime
            }

        return state

    def load_state(self):
        if not self.state_file.exists():
            return {}

        with open(self.state_file,  "r" ) as file:
            return json.load(file)

    def save_state( self, state):
        self.state_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(self.state_file, "w" ) as file:
            json.dump(
                state,
                file,
                indent=4
            )

    def has_changes(self):
        current = ( self.get_current_state())
        previous = ( self.load_state())
        return current != previous

