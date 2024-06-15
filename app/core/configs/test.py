from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIRERCTORY = Path(__file__).parent.parent


class SnowflakeSettings(BaseModel):
    WORKER_ID: int = 777


class DatabaseSettings(BaseModel):
    gen: SnowflakeSettings = SnowflakeSettings()

    URL: str = f"sqlite+aiosqlite:///{BASE_DIRERCTORY.parent/"tests"/"database"/"test_database.sqlite3"}"


class JWTSettings(BaseModel):
    ALGORITHM: Literal["HS256"] = "HS256"
    SECRET: str = "NOTASECRET"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30


class StateSettings(BaseModel):
    production: bool = True
    debug: bool = False
    test: bool = True


class AppSettings(BaseModel):
    name: str = "ushort"


class TestSettings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    state: StateSettings = StateSettings()


test_settings: TestSettings = TestSettings()
