from pathlib import Path

# --- Folders ---
PROJECT_DIR = Path(__file__).parent
DOCS_DIR = PROJECT_DIR / "data" / "documents"
CHROMA_DIR = PROJECT_DIR / "chroma_db"
# --- AI models (run by Ollama) ---
CHAT_MODEL = "llama3.2"
EMBED_MODEL = "nomic-embed-text"
# --- Database ---
COLLECTION_NAME = "acme_policies"
# --- Chunking and search ---
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 3
# --- Files we can read ---
SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}