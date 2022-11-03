from functools import cache

from pydantic import BaseSettings, Field


class _Settings(BaseSettings):
    debug: bool = Field(False, description="Toggle file watcher to restart server on change")
    host: str = "localhost"
    port: int = 8000
    static_content_dir: str = "static"

    class Config:
        env_file = ".env"
        case_sensitive = False


@cache
def get_settings() -> _Settings:
    """Provides an interface for accessing env variables."""
    return _Settings()
