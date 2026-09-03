"""
Application configuration.

All configuration is loaded from environment variables (see .env.example).
Nothing here should ever contain a hardcoded secret.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ---- Application ----
    app_name: str = "Patient Case Taking Software"
    app_env: str = "development"
    debug: bool = True

    # ---- Database ----
    database_url: str

    # ---- Security / JWT (used starting Phase 2) ----
    jwt_secret_key: str = "insecure-dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # ---- CORS ----
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # ---- File storage (used starting Phase 4) ----
    upload_dir: str = "./uploads"

    # ---- Speech service (used starting Phase 5) ----
    speech_provider: str = "bhashini"
    bhashini_api_key: str = ""
    bhashini_user_id: str = ""
    whisper_api_key: str = ""

    # ---- Logging ----
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> "Settings":
    """Cached settings instance — import and call this, don't instantiate Settings() directly."""
    return Settings()
