from pathlib import Path

from backend.core.configs.settings import (
    AppSettings,
    DatabaseSettings,
    JWTSettings,
    Settings,
    SnowflakeSettings,
    StateSettings,
)

BASE_DIRERCTORY = Path(__file__).parent.parent.parent.parent

snowflake_settings: SnowflakeSettings = SnowflakeSettings(
    WORKER_ID=888,
)

database_settings: DatabaseSettings = DatabaseSettings(
    gen=snowflake_settings,
    URL=f"sqlite+aiosqlite:///{BASE_DIRERCTORY/"tests"/"core"/"database"/"test_database.sqlite3"}",
)

jwt_settings: JWTSettings = JWTSettings(
    ALGORITHM="HS256",
    SECRET="",
    ACCESS_TOKEN_EXPIRE_MINUTES=60,
    REFRESH_TOKEN_EXPIRE_DAYS=30,
)

state_settings: StateSettings = StateSettings(
    PROD=True, # Lying about the state
    DEBUG=False,
    TEST=True,
)

app_settings: AppSettings = AppSettings(
    NAME="ushort",
)

test_settings: Settings = Settings(
    db=database_settings,
    jwt=jwt_settings,
    state=state_settings,
    app=app_settings,
)
