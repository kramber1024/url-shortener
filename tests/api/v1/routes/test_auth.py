from typing import TYPE_CHECKING

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import jwt_auth
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


@pytest.mark.asyncio()
async def test_authenticate_user(
    session: AsyncSession,
    client: AsyncClient,
) -> None:

    email: str = "Michael0@hotmail.com"
    password: str = "cU5EAv8itwutUO9"

    session.add(
        User(
            name="Destini_Hyatt52",
            email=email,
            password=password,
            salt_rounds=4,
        ),
    )
    await session.commit()

    json: dict[str, str] = {
        "email": email,
        "password": password,
    }

    response: Response = await client.post(
        "api/v1/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().keys()) == len(["access_token", "refresh_token"])
    assert response.json().get("access_token", "") != ""
    assert response.json().get("refresh_token", "") != ""


@pytest.mark.asyncio()
async def test_authenticate_user_incorrect_email(
    session: AsyncSession,
    client: AsyncClient,
) -> None:

    name: str = "Nathen_OConner"
    email: str = "Dusty_Klocko33@hotmail.com"
    password: str = "uZAsWQ6k_8uuQ2r"

    session.add(
        User(
            name=name,
            email=email,
            password=password,
            salt_rounds=4,
        ),
    )
    await session.commit()

    json: dict[str, str] = {
        "email": "Beth.Bernier@gmail.com",
        "password": password,
    }

    response: Response = await client.post(
        "api/v1/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert len(response.json().get("errors", "")) == 0
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_authenticate_user_incorrect_password(
    session: AsyncSession,
    client: AsyncClient,
) -> None:

    name: str = "Bessie Haag"
    email: str = "Marcel33@yahoo.com"
    password: str = "HNAzs_gQ4zGI2FF"

    session.add(
        User(
            name=name,
            email=email,
            password=password,
            salt_rounds=4,
        ),
    )
    await session.commit()

    json: dict[str, str] = {
        "email": email,
        "password": "mSdewoS6vAmL8LP",
    }

    response: Response = await client.post(
        "api/v1/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert len(response.json().get("errors", "")) == 0
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_authenticate_user_incorrect_all(
    session: AsyncSession,
    client: AsyncClient,
) -> None:

    name: str = "Eliezer_Hilll"
    email: str = "Ivy.Hammes7@yahoo.com"
    password: str = "YT5MqVCjlICQxLA"

    session.add(
        User(
            name=name,
            email=email,
            password=password,
            salt_rounds=4,
        ),
    )
    await session.commit()

    json: dict[str, str] = {
        "email": email + "ma",
        "password": password + "1",
    }

    response: Response = await client.post(
        "api/v1/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert len(response.json().get("errors", "")) == 0
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_authenticate_user_invalid_email(
    client: AsyncClient,
) -> None:

    email: str = "mymailllll.com"
    password: str = "OzjVn2XgleJ8Mo0"

    json: dict[str, str] = {
        "email": email,
        "password": password,
    }

    response: Response = await client.post(
        "api/v1/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", "")) == 1
    assert utils.error_type_exists(response.json(), "email")
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_authenticate_user_invalid_password(
    client: AsyncClient,
) -> None:

    email: str = "Marilou5@hotmail.com"
    password: str = "268"

    json: dict[str, str] = {
        "email": email,
        "password": password,
    }

    response: Response = await client.post(
        "api/v1/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", "")) == 1
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_authenticate_user_invalid_all(
    client: AsyncClient,
) -> None:

    name: str = "22"
    email: str = "Stanford81yahoocom"
    password: str = "YP2m6v"

    json: dict[str, str] = {
        "name": name,
        "email": email,
        "password": password,
    }

    response: Response = await client.post(
        "api/v1/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", "")) == len(["email", "password"])
    assert utils.error_type_exists(response.json(), "email")
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_authenticate_user_empty(
    client: AsyncClient,
) -> None:

    json: dict[str, str] = {}

    response: Response = await client.post(
        "api/v1/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", "")) == len(["email", "password"])
    assert utils.error_type_exists(response.json(), "email")
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_refresh_user(
    session: AsyncSession,
    client: AsyncClient,
) -> None:

    name: str = "Mrs. Alyssa Lueilwitz"
    email: str = "Maia_Osinski@hotmail.com"
    password: str = "G9rA8h3u5XUoqxn"

    user: User = User(
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    refresh_token: str = jwt_auth.generate_refresh_token(
        user_id=user.id,
        name=user.name,
        email=user.email,
    )

    response: Response = await client.post(
        "api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(["access_token", "refresh_token"])
    assert response.json().get("access_token", "") != ""
    assert response.json().get("refresh_token", "") != ""
    assert user
    assert isinstance(user, User)
    assert isinstance(user.id, int)
    assert user.name == name
    assert user.email == utils.format_email(email)
    assert user.password != password
    assert user.is_password_valid(password)
    assert user.active


@pytest.mark.asyncio()
async def test_refresh_user_invalid_token(
    client: AsyncClient,
) -> None:

    refresh_token: str = (
        "wnce8OakjfsPgNSWvlZosGgSWkXPhR."
        "19Q5n3vX04pJorG6Ps2LYzrmZr1Xdc."
        "fO43J2Amatx31wE9iLUDFcxm08KPva"
    )

    response: Response = await client.post(
        "api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(response.json().get("errors", "")) == 0
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_400_BAD_REQUEST
    assert response.json().get("access_token", "") == ""
    assert response.json().get("refresh_token", "") == ""


@pytest.mark.asyncio()
async def test_refresh_user_access_token(
    session: AsyncSession,
    client: AsyncClient,
) -> None:

    name: str = "Jermaine Howe"
    email: str = "Riley.Wilkinson91@yahoo.com"
    password: str = "NIucXOsGNhCXRkI"

    user: User = User(
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    access_token: str = jwt_auth.generate_access_token(
        user_id=user.id,
        name=user.name,
        email=user.email,
    )

    response: Response = await client.post(
        "api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(response.json().get("errors", "")) == 0
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_400_BAD_REQUEST
    assert response.json().get("access_token", "") == ""
    assert response.json().get("refresh_token", "") == ""


@pytest.mark.asyncio()
async def test_refresh_user_no_authorization(
    session: AsyncSession,
    client: AsyncClient,
) -> None:

    name: str = "Mrs. Geneva Kemmer"
    email: str = "Leonor60@gmail.com"
    password: str = "s8g_xP1R6a56y1C"

    user: User = User(
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    response: Response = await client.post(
        "api/v1/auth/refresh",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert len(response.json().get("errors", "")) == 0
    assert response.json().get("message", "") != ""
    assert response.json().get("status", 0) == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("access_token", "") == ""
    assert response.json().get("refresh_token", "") == ""
