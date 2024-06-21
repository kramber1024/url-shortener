from backend.core.configs.debug import debug_settings
from backend.core.configs.settings import Settings
from backend.core.configs.test import test_settings

settings: Settings = debug_settings

__all__ = (
    "settings"
    "debug_settings",
    "test_settings",
    "Settings",
)
