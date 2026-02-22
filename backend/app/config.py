from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://liquidity_user:password123@localhost:5434/liquidity_tracker"
    FRED_API_KEY: str = "demo"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]
    USE_MOCK_DATA: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
