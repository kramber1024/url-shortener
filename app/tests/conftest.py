from asyncio import current_task
from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.core.config import settings
from app.core.database import Database


@pytest_asyncio.fixture(scope="session")
async def db() -> AsyncGenerator[Database, None]:
    test_db: Database = Database(
        url=settings.test.db.URL,
        debug=False,
    )
    await test_db.create_db(hard_rest=True)
    yield test_db
    await test_db.engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(db: Database) -> AsyncGenerator[AsyncSession, None]:
    async_session: async_scoped_session[AsyncSession] = async_scoped_session(
        session_factory=db.session_factory,
        scopefunc=current_task,
    )

    try:
        async with async_session() as session:
            yield session

    finally:
        await async_session.remove()
