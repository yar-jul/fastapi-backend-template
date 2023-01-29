from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    VERSION: str = "0.1.0"
    TITLE: str = "API"
    DESCRIPTION: str = "API"
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_DSN: Optional[str] = None
    SQLALCHEMY_LOG_ALL: bool = False
    CORS_OPTIONS: dict = {
        "allow_origins": ["*"],
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "allow_credentials": True,
    }
    API_PREFIX: str = ""
    ROOT_PATH: str = ""


settings = Settings()
