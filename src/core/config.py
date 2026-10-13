from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Uncertainty-Aware RAG API"
    environment: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    
    # New: Database connection string (defaults to a local SQLite file)
    database_url: str = "sqlite:///./rag_system.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()