import os
from typing import List
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
class Settings(BaseSettings):
    app_name: str = "SDA API"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    flask_secret_key: str = os.getenv("FLASK_SECRET_KEY", "sda_secret_key_2024")
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:5174",
    ]
    firebase_credentials_path: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase-credentials.json")
    flask_debug: str = os.getenv("FLASK_DEBUG", "false")
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }
settings = Settings()