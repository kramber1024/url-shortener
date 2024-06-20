from typing import TYPE_CHECKING

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import User
from tests import utils

if TYPE_CHECKING:
    from httpx import Response
    from sqlalchemy.engine import Result


@pytest.mark.asyncio()
async def test_register_user(
    session: AsyncSession,
    client: AsyncClient,
) -> None:

    name: str = "Vernon Barton"
    email: str = "Alison_Rempel36@YAHOO.com"
    password: str = "2RFTO5_Wx3aFDni"

    json: dict[str, str] = {
        "name": name,
        "email": email,
        "password": password,
    }

    response: Response = await client.post(
        "api/v1/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json().get("errors", "")) == 0
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_201_CREATED
    assert user
    assert isinstance(user, User)
    assert isinstance(user.id, int)
    assert user.name == name
    assert user.email == utils.format_email(email)
    assert user.password != password
    assert user.is_password_valid(password)
    assert user.active


@pytest.mark.asyncio()
async def test_register_user_uppercase(
    session: AsyncSession,
    client: AsyncClient,
) -> None:

    name: str = "IDELLA_UPTON376"
    email: str = "PEARLIE8@EXAMPLE.NET"
    password: str = "MAMMMM_T3QJZ123"

    json: dict[str, str] = {
        "name": name,
        "email": email,
        "password": password,
    }

    response: Response = await client.post(
        "api/v1/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json().get("errors", "")) == 0
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_201_CREATED
    assert user
    assert isinstance(user, User)
    assert isinstance(user.id, int)
    assert user.name == name
    assert user.email == utils.format_email(email)
    assert user.password != password
    assert user.is_password_valid(password)
    assert user.active


@pytest.mark.asyncio()
async def test_register_user_email_conflict(
    session: AsyncSession,
    client: AsyncClient,
) -> None:

    name: str = "Julian49"
    email: str = "Alisha_Borer@hotmail.com"
    password: str = "2ePl_ncWd_Ea0Vg"

    user: User = User(
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    json: dict[str, str] = {
        "name": name,
        "email": email,
        "password": password,
    }

    response: Response = await client.post(
        "api/v1/auth/register",
        json=json,
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert len(response.json().get("errors", "")) == 0
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_409_CONFLICT
    assert user
    assert isinstance(user, User)
    assert isinstance(user.id, int)
    assert user.name == name
    assert user.email == utils.format_email(email)
    assert user.password != password
    assert user.is_password_valid(password)
    assert user.active


@pytest.mark.asyncio()
async def test_register_user_invalid_name(
    session: AsyncSession,
    client: AsyncClient,
) -> None:

    name: str = "12"
    email: str = "Leta.Hartmann@hotmail.com"
    password: str = "eSB7Y6DxFFFkckZ"

    json: dict[str, str] = {
        "name": name,
        "email": email,
        "password": password,
    }

    response: Response = await client.post(
        "api/v1/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(email)),
    )
    user: User | None = result.scalars().first()

    assert user is None
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", "")) == 1
    assert utils.error_type_exists(response.json(), "name")
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_register_user_invalid_email(
    client: AsyncClient,
) -> None:

    name: str = "Curtis Lehner"
    email: str = "mymail.com"
    password: str = "TIB5SMrQIfQx6Jo"

    json: dict[str, str] = {
        "name": name,
        "email": email,
        "password": password,
    }

    response: Response = await client.post(
        "api/v1/auth/register",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", "")) == 1
    assert utils.error_type_exists(response.json(), "email")
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_register_user_invalid_password(
    session: AsyncSession,
    client: AsyncClient,
) -> None:

    name: str = "Aglae_Upton"
    email: str = "Kamryn65@example.org"
    password: str = "1234567"

    json: dict[str, str] = {
        "name": name,
        "email": email,
        "password": password,
    }

    response: Response = await client.post(
        "api/v1/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(email)),
    )
    user: User | None = result.scalars().first()

    assert user is None
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", "")) == 1
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_register_user_invalid_all(
    client: AsyncClient,
) -> None:

    name: str = "12"
    email: str = "@example.org"
    password: str = "1234567"

    json: dict[str, str] = {
        "name": name,
        "email": email,
        "password": password,
    }

    response: Response = await client.post(
        "api/v1/auth/register",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", "")) == len(["name", "email", "password"])
    assert utils.error_type_exists(response.json(), "name")
    assert utils.error_type_exists(response.json(), "email")
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_register_user_empty(
    client: AsyncClient,
) -> None:

    json: dict[str, str] = {}

    response: Response = await client.post(
        "api/v1/auth/register",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", "")) == len(["name", "email", "password"])
    assert utils.error_type_exists(response.json(), "name")
    assert utils.error_type_exists(response.json(), "email")
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY
