from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class IDGeneratorSettings(BaseModel):
    WORKER_ID: int = 1023 # int in range [1, 1023]


class DatabaseSettings(BaseModel):
    gen: IDGeneratorSettings = IDGeneratorSettings()

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
