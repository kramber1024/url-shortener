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


@pytest.mark.asyncio()
async def test_register_user_email_conflict(
    session: AsyncSession,
    client: AsyncClient,
) -> None:
    name, email, password = utils.random_user_credentials()

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
    )

    response: Response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": name,
            "email": user.email,
            "password": user.password,
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
