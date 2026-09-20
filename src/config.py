"""Configuration manager for Paideia Genesis."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))

# Subdirectories
RAW_SOURCES_DIR = DATA_DIR / "raw_sources"
WIKI_DIR = DATA_DIR / "wiki"
ANKI_EXPORT_DIR = DATA_DIR / "anki_exports"
DB_PATH = DATA_DIR / "wiki_index.db"

# LLM Configuration
# Providers: 'mock' (offline deterministic for testing/demos), 'gemini', 'openai_compatible' (Ollama/vLLM on home GPUs)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# For home GPU rigs (vLLM, Ollama, LM Studio, etc.)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "dummy-key")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "llama3.1:8b")

# AnkiConnect configuration
ANKI_CONNECT_URL = os.getenv("ANKI_CONNECT_URL", "http://127.0.0.1:8765")

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
