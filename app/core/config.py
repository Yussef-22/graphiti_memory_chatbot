"""Typed application settings loaded from environment variables."""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized and validated application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_ignore_empty=True,
        extra="ignore",
    )

    app_name: str = "Graphiti Memory Chatbot"
    app_version: str = "0.1.0"
    app_environment: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = Field(default=8000, ge=1, le=65535)
    app_log_level: str = "INFO"

    falkordb_host: str = "localhost"
    falkordb_port: int = Field(default=6379, ge=1, le=65535)
    falkordb_username: str | None = None
    falkordb_password: str | None = None
    falkordb_graph_name: str = "graphiti_memory"
    falkordb_connect_timeout: float = Field(default=3.0, gt=0)

    # Gemini is used explicitly for every Graphiti AI component. Keeping these
    # settings here prevents Graphiti from falling back to its OpenAI defaults.
    gemini_api_key: SecretStr | None = None
    gemini_model: str = "gemini-3.5-flash-lite"
    gemini_embedding_model: str = "gemini-embedding-001"

    # The free Gemini tier has conservative rate limits. Serial execution is
    # slower, but makes the local demo substantially more reliable.
    semaphore_limit: int = Field(default=1, ge=1, le=10)
    memory_search_limit: int = Field(default=5, ge=1, le=20)
    chat_max_output_tokens: int = Field(default=1024, ge=128, le=8192)


@lru_cache
def get_settings() -> Settings:
    """Return one cached settings instance for the application process."""
    return Settings()
