import hashlib
import json
from pathlib import Path
from typing import List

from langchain_core.documents import Document as LCDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.config.settings import settings
from backend.loaders.pdf_loader import PDFLoader


class DocumentController:
    """
    Controlador para la gestión, verificación de alteraciones e indexación
    de documentos PDF usando el PDFLoader del proyecto.
    """

    def __init__(self, rag_service=None, vector_repository=None):
        self.rag_service = rag_service
        self.vector_repository = vector_repository
        self.pdf_loader = PDFLoader()

        # Carpeta donde residen los documentos normativos
        self.documents_dir = Path("data/documents")
        self.documents_dir.mkdir(parents=True, exist_ok=True)

        # Archivo de registro para detectar cambios/alteraciones en los PDFs
        self.hash_manifest_path = Path(settings.VECTORSTORE_PATH) / "file_hashes.json"

        # Al inicializar, procesar automáticamente la carpeta de documentos
        self.sync_and_index_folder()

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calcula el hash MD5 de un archivo para verificar si sufrió alteraciones."""
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _get_folder_hashes(self) -> dict:
        """Obtiene un diccionario con los nombres de archivo y sus respectivos hashes."""
        hashes = {}
        for pdf_file in self.documents_dir.glob("*.pdf"):
            hashes[pdf_file.name] = self._calculate_file_hash(pdf_file)
        return hashes

    def _has_changes(self, current_hashes: dict) -> bool:
        """Compara los hashes actuales con el manifiesto guardado para detectar cambios."""
        if not self.hash_manifest_path.exists():
            return True

        try:
            with open(self.hash_manifest_path, "r", encoding="utf-8") as f:
                saved_hashes = json.load(f)
            return current_hashes != saved_hashes
        except Exception:
            return True

    def _save_hashes(self, current_hashes: dict):
        """Guarda el registro de hashes actualizado."""
        self.hash_manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.hash_manifest_path, "w", encoding="utf-8") as f:
            json.dump(current_hashes, f, indent=4)

    def sync_and_index_folder(self):
        """
        Escanea 'data/documents/'. Si detecta archivos nuevos, modificados
        o eliminados, ejecuta la re-indexación usando PDFLoader.
        """
        pdf_files = list(self.documents_dir.glob("*.pdf"))
        if not pdf_files:
            print("ℹ️ [DocumentController] No hay documentos PDF en 'data/documents/'.")
            return

        current_hashes = self._get_folder_hashes()

        # Verificar si existen vectores guardados y si los archivos cambiaron
        if self.vector_repository and self.vector_repository.exists():
            if not self._has_changes(current_hashes):
                print("✅ [DocumentController] No hay cambios en 'data/documents/'. Usando VectorStore existente.")
                return

        print("🔄 [DocumentController] Se detectaron cambios en los PDFs. Procesando e indexando...")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        all_lc_documents: List[LCDocument] = []

        for pdf_path in pdf_files:
            try:
                print(f"📖 Cargando con PDFLoader: {pdf_path.name}")

                # 1. Usar tu PDFLoader nativo (devuelve lista de tu modelo Document)
                custom_docs = self.pdf_loader.load(pdf_path)

                # 2. Convertir a LCDocument para compatibilidad con LangChain Splitter & FAISS
                lc_docs = [
                    LCDocument(
                        page_content=doc.content,
                        metadata=doc.metadata
                    )
                    for doc in custom_docs
                ]

                # 3. Dividir en fragmentos pequeños
                chunks = text_splitter.split_documents(lc_docs)
                all_lc_documents.extend(chunks)

            except Exception as e:
                print(f"❌ Error procesando {pdf_path.name}: {e}")

        if self.vector_repository and all_lc_documents:
            print(f"⚙️ Generando embeddings para {len(all_lc_documents)} fragmentos...")
            self.vector_repository.create(all_lc_documents)
            self.vector_repository.save()
            self._save_hashes(current_hashes)
            print("✅ [DocumentController] Proceso finalizado y base vectorial guardada en disco.")

    def upload_document(self, uploaded_file) -> str:
        """
        Guarda un nuevo PDF subido desde la interfaz en 'data/documents/'
        y re-sincroniza el repositorio vectorial automáticamente.
        """
        file_path = self.documents_dir / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        print(f"📄 [DocumentController] Archivo guardado/actualizado: {uploaded_file.name}")

        # Sincronizar e indexar
        self.sync_and_index_folder()

        return uploaded_file.name

    def list_documents(self) -> List[str]:
        """Retorna la lista de todos los PDFs almacenados en data/documents/."""
        if not self.documents_dir.exists():
            return []
        return [f.name for f in self.documents_dir.glob("*.pdf")]