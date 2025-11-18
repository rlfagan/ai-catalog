"""
Configuration settings for the application
Using Pydantic Settings for environment variable management
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, validator
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    DEBUG: bool = Field(default=True, description="Debug mode")
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", description="Secret key for JWT")

    # Database
    POSTGRES_USER: str = Field(default="aicat_user", description="PostgreSQL user")
    POSTGRES_PASSWORD: str = Field(default="changeme123", description="PostgreSQL password")
    POSTGRES_DB: str = Field(default="aicat_db", description="PostgreSQL database name")
    POSTGRES_HOST: str = Field(default="db", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL port")
    DATABASE_URL: str | None = Field(default=None, description="Full database URL")

    # CORS
    BACKEND_CORS_ORIGINS: List[str] | str = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Model Catalog"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Data
    DATA_FILE_PATH: str = Field(default="/app/data/hf_models.jsonl", description="Path to JSONL data file")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from string or list"""
        if isinstance(v, str):
            if v.startswith("["):
                # Parse JSON array string
                return json.loads(v)
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError("CORS origins must be a list or comma-separated string")

    @property
    def database_url_computed(self) -> str:
        """Compute database URL if not provided"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
