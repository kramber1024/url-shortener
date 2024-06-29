from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIRERCTORY = Path(__file__).parent.parent


class SnowflakeSettings(BaseSettings):
    WORKER_ID: int = 999 # Value in range [1, 1023]


class DatabaseSettings(BaseSettings):
    gen: SnowflakeSettings = SnowflakeSettings()
    URL: str = f"sqlite+aiosqlite:///{BASE_DIRERCTORY/"database"/"database.sqlite3"}"


class JWTSettings(BaseSettings):
    ALGORITHM: Literal["HS256"] = "HS256"
    SECRET: Annotated[str, Field(env="JWT_SECRET")]
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRES_DAYS: int = 30


class StateSettings(BaseSettings):
    PRODUCTION: Annotated[bool, Field(env="PRODUCTION")]
    DEBUG: Annotated[bool, Field(env="DEBUG")]


class AppSettings(BaseSettings):
    NAME: str = "ushort"
    state: StateSettings = StateSettings() # type: ignore[call-arg]


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings() # type: ignore[call-arg]
    app: AppSettings = AppSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings: Settings = Settings()
