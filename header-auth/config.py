from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Header Auth API"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False

    api_key: str = "change-me-in-production"

    database_url: str = "sqlite:///./header_auth.db"

    cors_origins: List[str] = ["*"]
    api_prefix: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()