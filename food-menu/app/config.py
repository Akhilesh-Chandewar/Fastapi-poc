from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Food Menu API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    api_prefix: str = ""

    cors_origins: list[str] = ["*"]
    log_level: str = "INFO"
    request_timeout_seconds: float = 30.0


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
