from enum import Enum
from functools import cache

from pydantic import BaseSettings, Field


class ENVIRONMENT(Enum):
    """Defines the development environment"""

    PRODUCTION = 0
    DEVELOPMENT = 1


class _Settings(BaseSettings):
    debug: bool = Field(False, description="Toggle file watcher to restart server on change")
    host: str = Field("localhost", description="Host name")
    port: int = 8000
    static_content_dir: str = "./static"
    environment: ENVIRONMENT = Field(
        ENVIRONMENT.DEVELOPMENT,
        description="serves build files from the static_content_dir if environment is PRODUCTION",
    )

    class Config:
        case_sensitive = False


@cache
def get_settings() -> _Settings:
    """Provides an interface for accessing env variables."""
    return _Settings()
