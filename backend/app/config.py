from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-this-in-production"

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/liquidity_tracker"
    REDIS_URL: str = "redis://localhost:6379"

    # API Keys
    FRED_API_KEY: str = ""

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
