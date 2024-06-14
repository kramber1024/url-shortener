from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.tests import utils

if TYPE_CHECKING:
    from app.core.database.models import User


@pytest.mark.asyncio()
async def test_create_user(
    session: AsyncSession,
) -> None:
    name, email, password = utils.random_user_credentials()

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
    )

    assert isinstance(user.id, int)
    assert user.name == name
    assert user.email == email
    assert user.is_password_valid(password)
    assert user.active


@pytest.mark.asyncio()
async def test_get_user_by_email(
    session: AsyncSession,
) -> None:
    name, email, password = utils.random_user_credentials()

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
    )

    found_user: User | None = await crud.get_user_by_email(
        session=session,
        email=email,
    )

    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.name == name
    assert found_user.email == email
    assert found_user.is_password_valid(password)
    assert found_user.active


@pytest.mark.asyncio()
async def test_get_user_by_email_not_found(
    session: AsyncSession,
) -> None:
    name, email, password = utils.random_user_credentials()

    await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
    )

    not_found_user: User | None = await crud.get_user_by_email(
        session=session,
        email="email@notreal.tld;",
    )

    assert not_found_user is None


@pytest.mark.asyncio()
async def test_get_user_by_id(
    session: AsyncSession,
) -> None:
    name, email, password = utils.random_user_credentials()

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
    )

    found_user: User | None = await crud.get_user_by_id(
        session=session,
        _id=user.id,
    )

    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.name == name
    assert found_user.email == email
    assert found_user.is_password_valid(password)
    assert found_user.active


@pytest.mark.asyncio()
async def test_get_user_by_id_not_found(
    session: AsyncSession,
) -> None:
    name, email, password = utils.random_user_credentials()

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
    )

    found_user: User | None = await crud.get_user_by_id(
        session=session,
        _id=user.id-1,
    )

    assert found_user is None
