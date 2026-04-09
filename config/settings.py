"""
Configuration and settings for the Customer Support Agent
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import Streamlit for secrets access
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


def get_secret(key: str, default: str = "") -> str:
    """
    Get a secret from Streamlit secrets or environment variables
    
    Args:
        key: Secret/environment variable name
        default: Default value if not found
        
    Returns:
        Secret value or default
    """
    # Try Streamlit secrets first (for production on Streamlit Cloud)
    if HAS_STREAMLIT:
        try:
            return st.secrets.get(key, os.getenv(key, default)).strip()
        except:
            pass
    
    # Fall back to environment variables
    return os.getenv(key, default).strip()


class Settings:
    """Application settings"""

    # API Configuration
    OPENAI_API_KEY = get_secret("OPENAI_API_KEY", "")
    AZURE_OPENAI_API_KEY = get_secret("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT = get_secret("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    # Model Configuration
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # Document Processing
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K = int(os.getenv("TOP_K", "5"))

    # Paths
    DATA_DIR = "data"
    DOCUMENTS_DIR = os.path.join(DATA_DIR, "documents")
    VECTORSTORE_DIR = os.path.join(DATA_DIR, "vectorstore")

    # Application Configuration
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    MAX_HISTORY = 10
    DEMO_MODE = get_secret("DEMO_MODE", "False").lower() == "true"

    @staticmethod
    def has_valid_api_key():
        """Check if valid API key is configured"""
        openai_key = Settings.OPENAI_API_KEY
        azure_key = Settings.AZURE_OPENAI_API_KEY
        
        # Check if keys are not placeholder values
        if openai_key and not openai_key.startswith("your_"):
            return True
        if azure_key and not azure_key.startswith("your_"):
            return True
        
        return False

    @staticmethod
    def validate():
        """Validate required settings - but don't fail on startup"""
        # Create necessary directories
        os.makedirs(Settings.DOCUMENTS_DIR, exist_ok=True)
        os.makedirs(Settings.VECTORSTORE_DIR, exist_ok=True)

    def __init__(self):
        self.validate()
