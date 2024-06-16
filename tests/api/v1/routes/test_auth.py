from typing import TYPE_CHECKING

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from tests import utils
from tests.data import INVALID_USER_DATA, VALID_USER_DATA

if TYPE_CHECKING:
    from httpx import Response

    from app.core.database.models import User


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("name", "email", "password"),
    INVALID_USER_DATA,
)
async def test_register_user_validation_error(
    session: AsyncSession,
    client: AsyncClient,
    name: str,
    email: str,
    password: str,
) -> None:

    json: dict[str, str] = {}

    if name != "":
        json["name"] = name

    if email != "":
        json["email"] = email

    if password != "":
        json["password"] = password

    response: Response = await client.post(
        "/api/v1/auth/register",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    user: User | None = await crud.get_user_by_email(
        session=session,
        email=email,
    )

    assert user is None


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("name", "email", "password"),
    VALID_USER_DATA,
)
async def test_register_user_email_conflict(
    session: AsyncSession,
    client: AsyncClient,
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

    response: Response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": name[:-1] + "2",
            "email": email,
            "password": password[:-1] + "2",
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT

    found_user: User | None = await crud.get_user_by_email(
        session=session,
        email=utils.format_email(email),
    )

    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.name == user.name
    assert found_user.email == user.email
    assert found_user.password == user.password
    assert found_user.active == user.active


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("name", "email", "password"),
    VALID_USER_DATA,
)
async def test_register_user_success(
    session: AsyncSession,
    client: AsyncClient,
    name: str,
    email: str,
    password: str,
) -> None:

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
    ("name", "email", "password"),
    INVALID_USER_DATA,
)
async def test_authenticate_user_validation_error(
    session: AsyncSession,
    client: AsyncClient,
    name: str,
    email: str,
    password: str,
) -> None:

    json: dict[str, str] = {
        "name": name,
    }

    if email != "":
        json["email"] = email

    if password != "":
        json["password"] = password

    response: Response = await client.post(
        "/api/v1/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    user: User | None = await crud.get_user_by_email(
        session=session,
        email=email,
    )

    assert user is None


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("name", "email", "password"),
    VALID_USER_DATA,
)
async def test_authenticate_user_incorrect_credentials(
    session: AsyncSession,
    client: AsyncClient,
    name: str,
    email: str,
    password: str,
) -> None:

    formatted_email: str = utils.format_email(email)

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    response_1: Response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": formatted_email,
            "password": "12345678",
        },
    )

    assert response_1.status_code == status.HTTP_401_UNAUTHORIZED

    response_2: Response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": email[:-1] + "klol",
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
@pytest.mark.parametrize(
    ("name", "email", "password"),
    VALID_USER_DATA,
)
async def test_authenticate_user_success(
    session: AsyncSession,
    client: AsyncClient,
    name: str,
    email: str,
    password: str,
) -> None:

    formatted_email: str = utils.format_email(email)

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
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
