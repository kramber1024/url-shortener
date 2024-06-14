from asyncio import current_task
from collections.abc import AsyncGenerator

import httpx
import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.core.config import settings
from app.core.database import Database
from app.core.database.models import User


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


@pytest.fixture(name="async_client")
async def async_client(initialize_backend_test_application: fastapi.FastAPI) -> httpx.AsyncClient:  # type: ignore
    async with httpx.AsyncClient(
        app=initialize_backend_test_application,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
