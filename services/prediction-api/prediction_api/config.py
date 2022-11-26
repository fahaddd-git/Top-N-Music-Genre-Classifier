from functools import cache
from pathlib import Path

from pydantic import BaseSettings, Field


class _Settings(BaseSettings):
    debug: bool = Field(False, description="Toggle file watcher to restart server on change")
    host: str = "0.0.0.0"
    port: int = 8000
    static_content_dir: Path = Path(__file__).resolve().parent / "static"
    model_dir: Path = Path(__file__).resolve().parent / "model"
    labels_json: Path = Path(__file__).resolve().parent / "model/labels.json"

    class Config:
        case_sensitive = False


@cache
def get_settings() -> _Settings:
    """Provides an interface for accessing env variables."""
    return _Settings()
