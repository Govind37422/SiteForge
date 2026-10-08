import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Writable data dir: HF Spaces (/data) or local default
DATA_DIR_OVERRIDE = os.getenv("SITEFORGE_DATA_DIR")

PROVIDER = os.getenv("PROVIDER", "groq").lower()
API_KEY = os.getenv("OPENAI_API_KEY", "")

# Base URLs and Model mapping
PROVIDER_CONFIGS = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        "default_model": "llama-3.3-70b-versatile"
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "models": ["meta-llama/llama-3.3-70b-instruct", "openai/gpt-4o-mini", "google/gemini-flash-1.5"],
        "default_model": "meta-llama/llama-3.3-70b-instruct"
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "models": ["gpt-4o", "gpt-4o-mini"],
        "default_model": "gpt-4o"
    }
}

DB_PATH = Path(__file__).resolve().parent.parent / "siteforge_v2.db"
