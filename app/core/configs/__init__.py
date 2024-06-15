import os

from pydantic_settings import BaseSettings

from app.core.configs.debug import DebugSettings, debug_settings
from app.core.configs.test import AppSettings, test_settings


async def settings() -> BaseSettings:
    if bool(os.getenv("TEST")):
        return test_settings
    return debug_settings


__all__ = (
    "DebugSettings",
    "AppSettings",
    "settings",
)
