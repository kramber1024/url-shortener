from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core import settings

_engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URI,
    connect_args={"check_same_thread": False},
)
_session_local: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=_engine,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    database: AsyncSession = _session_local()

    try:
        yield database

    finally:
        await database.close()
