import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings:
    # GEMINI
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
    TEMPERATURE = 0.0

    # EMBEDDINGS
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
    DEVICE = "cpu"
    NORMALIZE_EMBEDDINGS = True

    # RUTAS
    DOCUMENTS_PATH = BASE_DIR / "data" / "documents"
    VECTORSTORE_PATH = BASE_DIR / "vectorstore"

    # RETRIEVER CONFIG
    TOP_K = 8
    NO_ANSWER = "No lo se!!"

settings = Settings()