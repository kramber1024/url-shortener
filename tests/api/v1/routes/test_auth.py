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


@pytest.mark.asyncio()
async def test_register_user_success(
    session: AsyncSession,
    client: AsyncClient,
) -> None:
    name, email, password = utils.random_user_credentials()
    formatted_email: str = utils.format_email(email)

    response: Response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    found_user: User | None = await crud.get_user_by_email(
        session=session,
        email=formatted_email,
    )

    assert found_user is not None
    assert found_user.name == name
    assert found_user.email == formatted_email
    assert found_user.password != password
    assert found_user.active


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("email", "password"), [
        (
            f"{utils.random_string(5)}@{utils.random_string(5)}", # Invalid email
            utils.random_string(16),
        ),
        (
            "", # Invalid email
            f"{utils.random_string(5)}@{utils.random_string(15)}",
        ),
        (
            utils.random_string(5), # Invalid email
            utils.random_string(1024), # Invalid password
        ),
        (
            utils.random_string_of_random_length(4, 16), # Invalid email
            utils.random_string(5), # Invalid password
        ),
        (
            None, None, # No email, and password
        ),
        (
            "", # Invalid email
            "", # Invalid password
        ),
    ],
)
async def test_authenticate_user_validation_error(
    session: AsyncSession,
    client: AsyncClient,
    email: str | None,
    password: str | None,
) -> None:

    json: dict[str, str] = {}

    if email is not None:
        json["email"] = email

    if password is not None:
        json["password"] = password

    response: Response = await client.post(
        "/api/v1/auth/login",
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
async def test_authenticate_user_incorrect_credentials(
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

    response_1: Response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password[:-5] + utils.random_string(5),
        },
    )

    assert response_1.status_code == status.HTTP_401_UNAUTHORIZED

    response_2: Response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": utils.random_email(),
            "password": password,
        },
    )

    assert response_2.status_code == status.HTTP_401_UNAUTHORIZED

    response_3: Response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": user.password,
        },
    )

    assert response_3.status_code == status.HTTP_401_UNAUTHORIZED

    found_user: User | None = await crud.get_user_by_email(
        session=session,
        email=formatted_email,
    )

    assert found_user is not None
    assert found_user.name == name
    assert found_user.email == formatted_email
    assert found_user.password != password
    assert found_user.active


@pytest.mark.asyncio()
async def test_authenticate_user_success(
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
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    response_body: dict[str, str] = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_body["access_token"]
    assert response_body["refresh_token"]
    assert isinstance(response_body["access_token"], str)
    assert isinstance(response_body["refresh_token"], str)

    found_user: User | None = await crud.get_user_by_email(
        session=session,
        email=formatted_email,
    )

    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.name == name
    assert found_user.email == formatted_email
    assert found_user.password != password
    assert found_user.active
