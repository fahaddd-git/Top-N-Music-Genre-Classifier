from pydantic import BaseSettings, Field


class _Settings(BaseSettings):
    debug: bool = Field(False, description="Toggle file watcher to restart server on change")
    host: str = Field("0.0.0.0", description="Host name")
    port: int = 8000
    static_content_dir: str = "../static"

    class Config:
        case_sensitive = False


global_settings = _Settings()
