from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./meeting_notes.db"
    VEXA_API_KEY: str
    VEXA_BASE_URL: str = "https://api.cloud.vexa.ai"
    OPENAI_API_KEY: str  # Keep this for backward compatibility
    GEMINI_API_KEY: str  # New Gemini API key
    SECRET_KEY: str
    CORS_ORIGINS: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"


settings = Settings()