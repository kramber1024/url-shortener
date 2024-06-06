from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TYPE: Literal["development", "production"] = "development"
    APP_NAME: str = "ushort"
    DEBUG: bool = bool(TYPE == "development")
    DATABASE_URI: str = "sqlite+aiosqlite:///./database/database.sqlite3"


settings: Settings = Settings()
