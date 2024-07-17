from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DebugSettings(BaseSettings):
    DEBUG_HOST: Annotated[
        str,
        Field(json_schema_extra={"env": "STATIC_SERVER_DEBUG_HOST"}),
    ] = "127.0.0.1"
    DEBUG_PORT: Annotated[
        int,
        Field(json_schema_extra={"env": "STATIC_SERVER_DEBUG_PORT"}),
    ] = 26999


class AppSettings(BaseSettings):
    NAME: Annotated[str, Field(json_schema_extra={"env": "APP_NAME"})] = ""


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    debug: DebugSettings = DebugSettings()

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings: Settings = Settings()
