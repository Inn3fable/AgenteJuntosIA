import os
from pathlib import Path
from detenv import load_detenv

load_detenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings:
    # ==========================
    # GEMINI
    # ==========================
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL","gemini-3.1-flash-lite")
    TEMPERATURE = 0

    # ==========================
    # EMBEDDINGS
    # ==========================
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL","BAAI/bge-m3")
    DEVICE = "cpu"
    NORMALIZE_EMBEDDINGS = True

    # ==========================
    # DOCUMENTOS
    # ==========================
    DOCUMENTS_PATH = (BASE_DIR / "data" / "documents")

    # ==========================
    # VECTOR STORE
    # ==========================
    VECTORSTORE_PATH = (BASE_DIR / "vectorstore")

    # ==========================
    # RETRIEVER CONFIG
    # ==========================
    SEARCH_TYPE = "similarity_score_threshold"
    TOP_K = 4
    SCORE_THRESHOLD = 0.1
    SEARCH_SCORE_THRESHOLD = 0.1

    # ==========================
    # RAG
    # ==========================
    NO_ANSWER = "No lo se!!"

settings = Settings()
