"""Configuration manager for Paideia Genesis."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# Detect if running as a compiled PyInstaller / frozen binary
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    BUNDLE_DIR = Path(sys._MEIPASS)
else:
    BUNDLE_DIR = Path(__file__).resolve().parent.parent

BASE_DIR = BUNDLE_DIR
DEMO_DATA_DIR = BUNDLE_DIR / "demo_data"
STATIC_DIR = BUNDLE_DIR / "static"

# Writable user runtime data directory (defaults to ./data relative to execution CWD)
DATA_DIR = Path(os.getenv("DATA_DIR", Path.cwd() / "data"))

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
# Local inference servers (Ollama, vLLM, LM Studio) typically don't require a real API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "llama3.1:8b")

# AnkiConnect configuration
ANKI_CONNECT_URL = os.getenv("ANKI_CONNECT_URL", "http://127.0.0.1:8765")

# TypeSafe AI / Jev "System One" Configuration
TYPESAFE_API_KEY = os.getenv("TYPESAFE_API_KEY", "")
ENABLE_JEV_SYSTEM_ONE = os.getenv("ENABLE_JEV_SYSTEM_ONE", "true").lower() in ("true", "1", "yes")

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Auto-seed demo curricula on empty database (defaults to false for clean research notebook setup)
AUTO_SEED_DEMO_DATA = os.getenv("AUTO_SEED_DEMO_DATA", "false").lower() in ("true", "1", "yes")


