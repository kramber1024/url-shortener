from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIRERCTORY = Path(__file__).parent.parent


class IDGeneratorSettings(BaseModel):
    WORKER_ID: int = 1023 # int in range [1, 1023]


class DatabaseSettings(BaseModel):
    gen: IDGeneratorSettings = IDGeneratorSettings()

    URL: str = f"sqlite+aiosqlite:///{BASE_DIRERCTORY/"core"/"database"/"database.sqlite3"}"


# TODO(kramber): Use env for sensitive data.
# 001
class JWTSettings(BaseModel):
    ALGORITHM: Literal["HS256"] = "HS256"
    SECRET: str = "4ede672801460916ec9f05540cf4325a9800c92e687df0846eeb87b8ad480a4e"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30


class AppSettings(BaseModel):
    NAME: str = "ushort"


class DebugSettings(BaseModel):
    IS_DEBUG: bool = True
    USER_NAME: str = "test"
    USER_EMAIL: str = "a@a.a"
    USER_PASSWORD: str = "12345678"


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    app: AppSettings = AppSettings()
    debug: DebugSettings = DebugSettings()
    jwt: JWTSettings = JWTSettings()


settings: Settings = Settings()
