from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core import settings


class Database:
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]

    def __init__(self, url: str, *, debug: bool) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=debug,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )


db: Database = Database(
    url=settings.db.URL,
    debug=settings.env.DEBUG,
)
