from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIRERCTORY = Path(__file__).parent.parent


class SnowflakeSettings(BaseModel):
    WORKER_ID: int = 888


class DatabaseSettings(BaseModel):
    gen: SnowflakeSettings = SnowflakeSettings()

    URL: str = f"sqlite+aiosqlite:///{BASE_DIRERCTORY/"app"/"core"/"database"/"database.sqlite3"}"


class JWTSettings(BaseModel):
    ALGORITHM: Literal["HS256"] = "HS256"
    SECRET: str = "NOTASECRET"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30


class StateSettings(BaseModel):
    production: bool = False
    debug: bool = True
    test: bool = False


class AppSettings(BaseModel):
    name: str = "ushort_d"


class DebugSettings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    app: AppSettings = AppSettings()
    state: StateSettings = StateSettings()


debug_settings: DebugSettings = DebugSettings()
