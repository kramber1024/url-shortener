from asyncio import current_task
from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.core.config import settings
from app.core.database import Database
from app.core.database import db as database
from app.core.database.models import User
from app.main import app


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
            await session.execute(delete(User))
            await session.commit()

    finally:
        await async_session.remove()


@pytest_asyncio.fixture(scope="function")
async def client(db: Database) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[database.scoped_session] = db.scoped_session

    async with AsyncClient(
        transport=ASGITransport(app=app), # type: ignore[arg-type]
        base_url="http://127.0.0.1:8000",
        headers={"Content-Type": "application/json"},
    ) as c:
        yield c

    app.dependency_overrides.clear()
