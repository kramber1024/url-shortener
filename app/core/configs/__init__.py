from app.core.configs.debug import debug_settings
from app.core.configs.settings import Settings
from app.core.configs.test import test_settings

settings: Settings = debug_settings

__all__ = (
    "settings"
    "debug_settings",
    "test_settings",
    "Settings",
)
