from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseModel):
    URL: str = "sqlite+aiosqlite:///./database/database.sqlite3"


class AppSettings(BaseModel):
    NAME: str = "ushort"


class EnviromentSettings(BaseModel):
    TYPE: Literal["development", "production"] = "development"
    DEBUG: bool = bool(TYPE == "development")


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    app: AppSettings = AppSettings()
    env: EnviromentSettings = EnviromentSettings()


settings: Settings = Settings()
