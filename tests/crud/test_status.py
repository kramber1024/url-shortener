import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend import crud
from backend.core.database.models import Status, User


@pytest.mark.asyncio()
async def test_create_status(
    session: AsyncSession,
    db_user: User,
) -> None:

    status: Status = await crud.create_status(
        session=session,
        user_id=db_user.id,
    )

    assert status.user_id == db_user.id
    assert status.email_verified is False
    assert status.phone_verified is False
    assert status.active is True
    assert status.premium is False


@pytest.mark.asyncio()
async def test_create_status_inactive(
    session: AsyncSession,
    db_user: User,
) -> None:

    status: Status = await crud.create_status(
        session=session,
        user_id=db_user.id,
        active=False,
    )

    assert status.user_id == db_user.id
    assert status.email_verified is False
    assert status.phone_verified is False
    assert status.active is False
    assert status.premium is False


@pytest.mark.asyncio()
async def test_create_status_premium(
    session: AsyncSession,
    db_user: User,
) -> None:

    status: Status = await crud.create_status(
        session=session,
        user_id=db_user.id,
        premium=True,
    )

    assert status.user_id == db_user.id
    assert status.email_verified is False
    assert status.phone_verified is False
    assert status.active is True
    assert status.premium is True
