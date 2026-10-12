from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Uncertainty-Aware RAG API"
    environment: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    # Automatically read from a .env file if it exists
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Instantiate a global settings object to be imported across the app
settings = Settings()