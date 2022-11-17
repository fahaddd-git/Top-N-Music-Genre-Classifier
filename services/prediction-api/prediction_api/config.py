from functools import cache
from pathlib import Path

from pydantic import BaseConfig, BaseSettings, Field


class _Settings(BaseSettings):
    debug: bool = Field(False, description="Toggle file watcher to restart server on change")
    host: str = "localhost"
    port: int = 8000
    static_content_dir: Path = Path(__file__).resolve().parent / "static"
    model_dir: Path = Path(__file__).resolve().parent / "model"
    labels_json: Path = Path(__file__).resolve().parent / "model/labels.json"

    class Config(BaseConfig):
        env_file = "../.env", ".env"
        case_sensitive = False


@cache
def get_settings() -> _Settings:
    """Provides an interface for accessing env variables."""
    return _Settings()
