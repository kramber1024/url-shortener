import datetime
from typing import TYPE_CHECKING, Literal

import jwt
import pytest
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.v1.exceptions import ErrorException
from app.core.auth import jwt_auth
from app.core.configs import test_settings
from tests.data import (
    INVALID_USER_DATA,
    JWT_CREDENTIALS,
    JWT_TOKENS,
    USER_INFO,
    VALID_USER_DATA,
)

if TYPE_CHECKING:
    from app.core.database.models import User


@pytest.mark.parametrize(
    ("jwt_type", "payload"),
    JWT_CREDENTIALS,
)
def test__encode_jwt(
    jwt_type: Literal["access", "refresh"],
    payload: dict[str, str | int],
) -> None:

    payload = payload.copy()

    token: str = jwt_auth._encode_jwt(
        jwt_type=jwt_type,
        payload=payload,
    )

    decoded_headers: dict[str, str] = jwt.get_unverified_header(token)
    decoded_payload: dict[str, str | int] = jwt.decode(
        token,
        key=test_settings.jwt.SECRET,
        algorithms=[test_settings.jwt.ALGORITHM],
    )

    assert "alg" in decoded_headers
    assert "typ" in decoded_headers
    assert decoded_headers["alg"] == test_settings.jwt.ALGORITHM
    assert decoded_headers["typ"] == jwt_type
    assert "sub" in decoded_payload
    assert "name" in decoded_payload
    assert "email" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert "key" in decoded_payload
    assert decoded_payload["sub"] == payload["sub"]
    assert decoded_payload["name"] == payload["name"]
    assert decoded_payload["email"] == payload["email"]
    assert isinstance(decoded_payload["exp"], int)
    assert isinstance(decoded_payload["iat"], int)
    assert decoded_payload["key"] == payload["key"]


@pytest.mark.parametrize(
    ("user_id", "name", "email"),
    USER_INFO,
)
def test_generate_access_token(
    user_id: int,
    name: str,
    email: str,
) -> None:

    token: str = jwt_auth.generate_access_token(
        user_id=user_id,
        name=name,
        email=email,
    )

    decoded_headers: dict[str, str] = jwt.get_unverified_header(token)
    decoded_payload: dict[str, str | int] = jwt.decode(
        token,
        key=test_settings.jwt.SECRET,
        algorithms=[test_settings.jwt.ALGORITHM],
    )

    assert "alg" in decoded_headers
    assert "typ" in decoded_headers
    assert decoded_headers["alg"] == test_settings.jwt.ALGORITHM
    assert decoded_headers["typ"] == "access"
    assert "sub" in decoded_payload
    assert "name" in decoded_payload
    assert "email" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert decoded_payload["sub"] == str(user_id)
    assert decoded_payload["name"] == name
    assert decoded_payload["email"] == email
    assert isinstance(decoded_payload["exp"], int)
    assert isinstance(decoded_payload["iat"], int)


@pytest.mark.parametrize(
    ("user_id", "name", "email"),
    USER_INFO,
)
def test_generate_refresh_token(
    user_id: int,
    name: str,
    email: str,
) -> None:

    token: str = jwt_auth.generate_refresh_token(
        user_id=user_id,
        name=name,
        email=email,
    )

    decoded_headers: dict[str, str] = jwt.get_unverified_header(token)
    decoded_payload: dict[str, str | int] = jwt.decode(
        token,
        key=test_settings.jwt.SECRET,
        algorithms=[test_settings.jwt.ALGORITHM],
    )

    assert "alg" in decoded_headers
    assert "typ" in decoded_headers
    assert decoded_headers["alg"] == test_settings.jwt.ALGORITHM
    assert decoded_headers["typ"] == "refresh"
    assert "sub" in decoded_payload
    assert "name" in decoded_payload
    assert "email" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert decoded_payload["sub"] == str(user_id)
    assert decoded_payload["name"] == name
    assert decoded_payload["email"] == email
    assert isinstance(decoded_payload["exp"], int)
    assert isinstance(decoded_payload["iat"], int)


@pytest.mark.parametrize(
    ("user_id", "name", "email"),
    USER_INFO,
)
def test_get_token_payload_access(
    user_id: int,
    name: str,
    email: str,
) -> None:

    token: str = jwt_auth.generate_access_token(
        user_id=user_id,
        name=name,
        email=email,
    )

    headers: dict[str, str] = jwt.get_unverified_header(token)
    payload: dict[str, str | int] | None = jwt_auth.get_token_payload(
        token=token,
        jwt_type="access",
    )

    assert payload is not None
    assert "alg" in headers
    assert "typ" in headers
    assert headers["alg"] == test_settings.jwt.ALGORITHM
    assert headers["typ"] == "access"
    assert "sub" in payload
    assert "name" in payload
    assert "email" in payload
    assert "exp" in payload
    assert "iat" in payload
    assert payload["sub"] == str(user_id)
    assert payload["name"] == name
    assert payload["email"] == email
    assert isinstance(payload["exp"], int)
    assert isinstance(payload["iat"], int)


@pytest.mark.parametrize(
    ("user_id", "name", "email"),
    USER_INFO,
)
def test_get_token_payload_refresh(
    user_id: int,
    name: str,
    email: str,
) -> None:

    token: str = jwt_auth.generate_refresh_token(
        user_id=user_id,
        name=name,
        email=email,
    )

    headers: dict[str, str] = jwt.get_unverified_header(token)
    payload: dict[str, str | int] | None = jwt_auth.get_token_payload(
        token=token,
        jwt_type="refresh",
    )

    assert payload is not None
    assert "alg" in headers
    assert "typ" in headers
    assert headers["alg"] == test_settings.jwt.ALGORITHM
    assert headers["typ"] == "refresh"
    assert "sub" in payload
    assert "name" in payload
    assert "email" in payload
    assert "exp" in payload
    assert "iat" in payload
    assert payload["sub"] == str(user_id)
    assert payload["name"] == name
    assert payload["email"] == email
    assert isinstance(payload["exp"], int)
    assert isinstance(payload["iat"], int)


@pytest.mark.parametrize(
    ("jwt_type", "token"),
    JWT_TOKENS,
)
def test_get_token_payload_invalid_token(
    jwt_type: Literal["access", "refresh"],
    token: str,
) -> None:
    payload: dict[str, str | int] | None = jwt_auth.get_token_payload(
        token=token,
        jwt_type=jwt_type,
    )

    assert payload is None


@pytest.mark.parametrize(
    ("jwt_type", "payload"),
    JWT_CREDENTIALS,
)
def test_get_token_payload_invalid_signature(
    jwt_type: Literal["access", "refresh"],
    payload: dict[str, str | int],
) -> None:
    key: str = "fx}rYFG$av/=kZmANt-(ee_;%SBZUy"*100

    now: int = int(datetime.datetime.now(datetime.UTC).timestamp())

    payload = payload.copy()
    payload.update(
        {
            "exp": now+24*60*60,
            "iat": now-24*60*60,
        },
    )

    token: str = jwt.encode(
        payload,
        key,
        test_settings.jwt.ALGORITHM,
        headers={
            "typ": jwt_type,
        },
    )

    decoded_payload: dict[str, str | int] | None = jwt_auth.get_token_payload(
        token=token,
        jwt_type=jwt_type,
    )

    assert decoded_payload is None


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("name", "email", "password"),
    VALID_USER_DATA + INVALID_USER_DATA,
)
async def test_get_current_user(
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

    token: str = jwt_auth.generate_access_token(
        user_id=user.id,
        name=user.name,
        email=user.email,
    )

    current_user: User = await jwt_auth.get_current_user(
        session=session,
        token=HTTPAuthorizationCredentials(scheme="Bearer", credentials=token),
    )

    assert current_user is not None
    assert current_user.id == user.id
    assert current_user.name == user.name
    assert current_user.email == user.email
    assert current_user.password != password
    assert current_user.is_password_valid(password)
    assert current_user.active == user.active


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("name", "email", "password"),
    VALID_USER_DATA + INVALID_USER_DATA,
)
async def test_get_current_user_invalid_token(
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

    with pytest.raises(ErrorException) as exc_info:
        await jwt_auth.get_current_user(
            session=session,
            token=HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials=f"{name}.{email}.{password}",
            ),
        )

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
