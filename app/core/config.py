import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Personalized Chat Bot"
    MONGO_DETAILS: Optional[str] = None
    DATABASE_NAME: Optional[str] = "chatbot_db"

    JWT_SECRET_KEY: str = "your_super_secret_key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 1 day

    # Gemini API Key
    GEMINI_API_KEY: Optional[str] = None

    # Allow extra fields for environment variables
    GOOGLE_API_KEY: str = "AIzaSyDb5JZuSD9KJykV0BFx-GFx6hEmWP9ZHfY"
    MONGO_DB_CONNECTION_STRING: str = "mongodb+srv://ansuman-shukla:ansuman@cluster0.zkpcq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Default LLM models
    DEFAULT_LLM_MODEL: str = "gemini-2.0-flash-lite" # Default model
    REASONING_LLM_MODEL: str = "gemini-2.5-pro-preview-05-06" # Model for reasoning
    NON_REASONING_LLM_MODEL: str = "gemini-2.0-flash-lite" # Default model

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # Allow extra fields

    def __init__(self, **data):
        super().__init__(**data)
        # Set GEMINI_API_KEY from GOOGLE_API_KEY if not set
        if not self.GEMINI_API_KEY and self.GOOGLE_API_KEY:
            self.GEMINI_API_KEY = self.GOOGLE_API_KEY

        # Set MONGO_DETAILS from MONGO_DB_CONNECTION_STRING if not set
        if not self.MONGO_DETAILS and self.MONGO_DB_CONNECTION_STRING:
            self.MONGO_DETAILS = self.MONGO_DB_CONNECTION_STRING

settings = Settings()

