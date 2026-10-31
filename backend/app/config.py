from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    OLLAMA_BASE_URL: str = Field(default="http://127.0.0.1:11434", description="Base URL for Ollama API")
    MODEL_NAME: str = Field(default="qwen:7b", description="Default model name to use for analysis")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    return Settings()
