from typing import TYPE_CHECKING

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from tests import utils

if TYPE_CHECKING:
    from httpx import Response

    from app.core.database.models import User


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("name", "email", "password"), [
        (
            f"{utils.random_string(5)}\n{utils.random_string(5)}",
            utils.random_string(8), # Invalid email
            utils.random_string(8),
        ),
        (
            "", # Invalid name
            f"{utils.random_string(5)}@{utils.random_string(15)}", # Invalid email
            utils.random_string(8),
        ),
        (
            utils.random_string(5),
            utils.random_email(max_length=64),
            utils.random_string(5), # Invalid password
        ),
        (
            utils.random_string_of_random_length(4, 16),
            utils.random_string(5), # Invalid email
            None, # No password
        ),
        (
            None, None, None, # No name, email, and password
        ),
        (
            None, # No name
            None, # No email
            utils.random_string_of_random_length(32, 64),
        ),
    ],
)
async def test_register_user_validation_error(
    session: AsyncSession,
    client: AsyncClient,
    name: str | None,
    email: str | None,
    password: str | None,
) -> None:
    json: dict[str, str] = {}

    if name is not None:
        json["name"] = name

    if email is not None:
        json["email"] = email

    if password is not None:
        json["password"] = password

    response: Response = await client.post(
        "/api/v1/auth/register",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    email = "" if email is None else email

    user: User | None = await crud.get_user_by_email(
        session=session,
        email=email,
    )

    assert user is None


@pytest.mark.asyncio()
async def test_register_user_email_conflict(
    session: AsyncSession,
    client: AsyncClient,
) -> None:
    name, email, password = utils.random_user_credentials()
    formatted_email: str = utils.format_email(email)

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
    )

    response: Response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": utils.random_string_of_random_length(4, 16),
            "email": email,
            "password": utils.random_string_of_random_length(32, 64),
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT

    found_user: User | None = await crud.get_user_by_email(
        session=session,
        email=formatted_email,
    )

    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.name == user.name
    assert found_user.email == user.email
    assert found_user.password == user.password
    assert found_user.active == user.active
