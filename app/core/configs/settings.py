from typing import Literal

from pydantic import BaseModel


class SnowflakeSettings(BaseModel):
    WORKER_ID: int


class DatabaseSettings(BaseModel):
    gen: SnowflakeSettings
    URL: str


class JWTSettings(BaseModel):
    ALGORITHM: Literal["HS256"]
    SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int


class StateSettings(BaseModel):
    PROD: bool
    DEBUG: bool
    TEST: bool


class AppSettings(BaseModel):
    NAME: str


class Settings(BaseModel):
    db: DatabaseSettings
    jwt: JWTSettings
    state: StateSettings
    app: AppSettings
