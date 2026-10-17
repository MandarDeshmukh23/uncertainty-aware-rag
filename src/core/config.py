from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Uncertainty-Aware RAG API"
    environment: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    
    database_url: str = "sqlite:///./rag_system.db"
    celery_broker_url: str = "amqp://guest:guest@localhost:5672//"
    
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    embedding_model_name: str = "all-MiniLM-L6-v2"
    
    # New: Local LLM configurations
    llm_base_url: str = "http://localhost:11434/v1" # Ollama's OpenAI-compatible endpoint
    llm_model_name: str = "llama3.2:1b"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()