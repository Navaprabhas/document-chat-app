"""
Configuration management for Document Chat Application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys - Note: These are read from environment at runtime
    # For user-entered keys, they are set in os.environ by the app
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google")  # "openai", "google", or "ollama"
    
    # OpenAI Settings
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Google Settings
    GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "models/gemini-2.5-flash")
    GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-2-preview")
    
    # Ollama Settings
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
    OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
    
    # Embedding Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "google")  # "openai", "google", or "ollama"
    
    # Vector Store Configuration
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./faiss_store")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "document_chat")
    
    # Document Processing
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # RAG Configuration
    TOP_K = int(os.getenv("TOP_K", "5"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "10"))
    
    # Application Settings
    TEMP_DIR = Path("temp")
    TEMP_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        errors = []
        
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required when using OpenAI")
        
        if cls.LLM_PROVIDER == "google" and not cls.GOOGLE_API_KEY:
            errors.append("GOOGLE_API_KEY is required when using Google")
        
        if cls.EMBEDDING_MODEL == "openai" and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required for OpenAI embeddings")
        
        if cls.EMBEDDING_MODEL == "google" and not cls.GOOGLE_API_KEY:
            errors.append("GOOGLE_API_KEY is required for Google embeddings")
        
        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))
        
        return True
    
    @classmethod
    def get_info(cls) -> dict:
        """Get configuration information (safe for display)"""
        return {
            "LLM Provider": cls.LLM_PROVIDER,
            "Model": cls.GOOGLE_MODEL if cls.LLM_PROVIDER == "google" else (cls.OPENAI_MODEL if cls.LLM_PROVIDER == "openai" else cls.OLLAMA_MODEL),
            "Embedding Model": cls.EMBEDDING_MODEL,
            "Chunk Size": cls.CHUNK_SIZE,
            "Chunk Overlap": cls.CHUNK_OVERLAP,
            "Top K Results": cls.TOP_K,
            "Temperature": cls.TEMPERATURE
        }
