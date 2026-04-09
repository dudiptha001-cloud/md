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
            value = st.secrets.get(key)
            if value:
                return str(value).strip()
        except Exception:
            pass
    
    # Fall back to environment variables
    value = os.getenv(key, default)
    return str(value).strip() if value else ""


class Settings:
    """Application settings with lazy loading for Streamlit secrets"""

    # Model Configuration (static)
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # Document Processing (static)
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K = int(os.getenv("TOP_K", "5"))

    # Paths (static)
    DATA_DIR = "data"
    DOCUMENTS_DIR = os.path.join(DATA_DIR, "documents")
    VECTORSTORE_DIR = os.path.join(DATA_DIR, "vectorstore")

    # Application Configuration (static)
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    MAX_HISTORY = 10
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    @classmethod
    def get_openai_api_key(cls) -> str:
        """Get OpenAI API key (lazy loaded)"""
        return get_secret("OPENAI_API_KEY", "")

    @classmethod
    def get_azure_api_key(cls) -> str:
        """Get Azure OpenAI API key (lazy loaded)"""
        return get_secret("AZURE_OPENAI_API_KEY", "")

    @classmethod
    def get_azure_endpoint(cls) -> str:
        """Get Azure OpenAI endpoint (lazy loaded)"""
        return get_secret("AZURE_OPENAI_ENDPOINT", "")

    @classmethod
    def get_demo_mode(cls) -> bool:
        """Get demo mode flag (lazy loaded)"""
        return get_secret("DEMO_MODE", "False").lower() == "true"

    # Backward compatibility properties
    @property
    def OPENAI_API_KEY(self) -> str:
        """Backward compatibility property"""
        return self.get_openai_api_key()

    @property
    def AZURE_OPENAI_API_KEY(self) -> str:
        """Backward compatibility property"""
        return self.get_azure_api_key()

    @property
    def AZURE_OPENAI_ENDPOINT(self) -> str:
        """Backward compatibility property"""
        return self.get_azure_endpoint()

    @property
    def DEMO_MODE(self) -> bool:
        """Backward compatibility property"""
        return self.get_demo_mode()

    @staticmethod
    def has_valid_api_key():
        """Check if valid API key is configured"""
        openai_key = Settings.get_openai_api_key()
        azure_key = Settings.get_azure_api_key()
        
        # Check if keys are not placeholder values or empty
        if openai_key and not openai_key.startswith("your_") and openai_key != "":
            return True
        if azure_key and not azure_key.startswith("your_") and azure_key != "":
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
