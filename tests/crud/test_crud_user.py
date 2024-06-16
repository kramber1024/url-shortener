from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from tests.data import INVALID_USER_DATA, VALID_USER_DATA
from tests.utils import format_email

if TYPE_CHECKING:
    from app.core.database.models import User


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("name", "email", "password"),
    INVALID_USER_DATA + VALID_USER_DATA,
)
async def test_create_user(
    session: AsyncSession,
    name: str,
    email: str,
    password: str,
) -> None:

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    assert user is not None
    assert isinstance(user.id, int)
    assert user.name == name
    assert user.email == format_email(email)
    assert user.password != password
    assert user.is_password_valid(password)
    assert user.active


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("name", "email", "password"),
    INVALID_USER_DATA + VALID_USER_DATA,
)
async def test_get_user_by_email(
    session: AsyncSession,
    name: str,
    email: str,
    password: str,
) -> None:

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    found_user: User | None = await crud.get_user_by_email(
        session=session,
        email=format_email(email),
    )

    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.name == user.name
    assert found_user.email == user.email
    assert found_user.password != password
    assert found_user.is_password_valid(password)
    assert found_user.active == user.active


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("name", "email", "password"),
    INVALID_USER_DATA + VALID_USER_DATA,
)
async def test_get_user_by_email_not_found(
    session: AsyncSession,
    name: str,
    email: str,
    password: str,
) -> None:

    await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    found_user: User | None = await crud.get_user_by_email(
        session=session,
        email=email + ";",
    )

    assert found_user is None


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("name", "email", "password"),
    INVALID_USER_DATA + VALID_USER_DATA,
)
async def test_get_user_by_id(
    session: AsyncSession,
    name: str,
    email: str,
    password: str,
) -> None:

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    found_user: User | None = await crud.get_user_by_id(
        session=session,
        _id=user.id,
    )

    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.name == user.name
    assert found_user.email == user.email
    assert found_user.password != password
    assert found_user.is_password_valid(password)
    assert found_user.active == user.active


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("name", "email", "password"),
    INVALID_USER_DATA + VALID_USER_DATA,
)
async def test_get_user_by_id_not_found(
    session: AsyncSession,
    name: str,
    email: str,
    password: str,
) -> None:

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    found_user: User | None = await crud.get_user_by_id(
        session=session,
        _id=user.id-1,
    )

    assert found_user is None
