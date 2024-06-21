import datetime
from typing import TYPE_CHECKING

import jwt
import pytest
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from backend import crud
from backend.api.v1.exceptions import ErrorException
from backend.core.auth import jwt_auth
from backend.core.configs import test_settings

if TYPE_CHECKING:
    from backend.core.database.models import User


def test__encode_jwt_access() -> None:
    id_: int = 7207503858480705536
    name: str = "Test User"
    email: str = "Christopher.Bins@gmail.com"
    extra_value: str = "MMezg[m)6/3n@H5#-Q#y,d?0tS4%K/"

    payload: dict[str, str | int] = {
        "sub": id_,
        "name": name,
        "email": email,
        "key": extra_value,
    }

    token: str = jwt_auth._encode_jwt(
        jwt_type="access",
        payload=payload,
        key=test_settings.jwt.SECRET,
        algorithm=test_settings.jwt.ALGORITHM,
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
    assert "key" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert decoded_payload["sub"] == id_
    assert decoded_payload["name"] == name
    assert decoded_payload["email"] == email
    assert decoded_payload["key"] == extra_value
    assert decoded_payload["exp"] in range(
        int(decoded_payload["iat"]),
        int(decoded_payload["iat"])+test_settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES*61,
    )
    assert decoded_payload["iat"] in range(
        int(datetime.datetime.now(datetime.UTC).timestamp()),
        int(datetime.datetime.now(datetime.UTC).timestamp())+61,
    )


def test__encode_jwt_refresh() -> None:
    id_: int = 12784851890751982875
    name: str = "John Doe"
    email: str = "Selena.Abshire54@yahoo.com"
    extra_value: str = "MMezg[m)6/3n@H5#-Q#y,d?0tS4%K/"

    payload: dict[str, str | int] = {
        "sub": id_,
        "name": name,
        "email": email,
        "key": extra_value,
    }

    token: str = jwt_auth._encode_jwt(
        jwt_type="refresh",
        payload=payload,
        key=test_settings.jwt.SECRET,
        algorithm=test_settings.jwt.ALGORITHM,
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
    assert "key" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert decoded_payload["sub"] == id_
    assert decoded_payload["name"] == name
    assert decoded_payload["email"] == email
    assert decoded_payload["key"] == extra_value
    assert decoded_payload["exp"] in range(
        int(decoded_payload["iat"]),
        int(decoded_payload["iat"])+test_settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS*24*60*61,
    )
    assert decoded_payload["iat"] in range(
        int(datetime.datetime.now(datetime.UTC).timestamp()),
        int(datetime.datetime.now(datetime.UTC).timestamp())+60,
    )


def test_generate_access_token() -> None:
    id_: int = 5912831238129485691
    name: str = "User Testing"
    email: str = "test@mail.tld"

    token: str = jwt_auth.generate_access_token(
        user_id=id_,
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
    assert decoded_payload["sub"] == str(id_)
    assert decoded_payload["name"] == name
    assert decoded_payload["email"] == email
    assert decoded_payload["exp"] in range(
        int(decoded_payload["iat"]),
        int(decoded_payload["iat"])+test_settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES*61,
    )
    assert decoded_payload["iat"] in range(
        int(datetime.datetime.now(datetime.UTC).timestamp()),
        int(datetime.datetime.now(datetime.UTC).timestamp())+61,
    )


def test_generate_refresh_token() -> None:
    id_: int = 5198519521092952920
    name: str = "Bob Smith"
    email: str = "C.hyouMao@Extraville.fi"

    token: str = jwt_auth.generate_refresh_token(
        user_id=id_,
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
    assert decoded_payload["sub"] == str(id_)
    assert decoded_payload["name"] == name
    assert decoded_payload["email"] == email
    assert decoded_payload["exp"] in range(
        int(decoded_payload["iat"]),
        int(decoded_payload["iat"])+test_settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS*24*60*61,
    )
    assert decoded_payload["iat"] in range(
        int(datetime.datetime.now(datetime.UTC).timestamp()),
        int(datetime.datetime.now(datetime.UTC).timestamp())+60,
    )


def test_get_token_payload_access() -> None:
    id_: int = 5812759129569819283980
    name: str = "Valerie Dodier"
    email: str = "Valerie@Dodier.fi"

    token: str = jwt_auth.generate_access_token(
        user_id=id_,
        name=name,
        email=email,
    )

    decoded_headers: dict[str, str] = jwt.get_unverified_header(token)
    decoded_payload: dict[str, str | int] | None = jwt_auth.get_token_payload(
        token=token,
        jwt_type="access",
    )

    assert decoded_payload
    assert "alg" in decoded_headers
    assert "typ" in decoded_headers
    assert decoded_headers["alg"] == test_settings.jwt.ALGORITHM
    assert decoded_headers["typ"] == "access"
    assert "sub" in decoded_payload
    assert "name" in decoded_payload
    assert "email" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert decoded_payload["sub"] == str(id_)
    assert decoded_payload["name"] == name
    assert decoded_payload["email"] == email
    assert int(decoded_payload["exp"]) in range(
        int(decoded_payload["iat"]),
        int(decoded_payload["iat"])+test_settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES*61,
    )
    assert int(decoded_payload["iat"]) in range(
        int(datetime.datetime.now(datetime.UTC).timestamp()),
        int(datetime.datetime.now(datetime.UTC).timestamp())+61,
    )


def test_get_token_payload_refresh() -> None:
    id_: int = 5871839859918235490
    name: str = "Smith Johnson"
    email: str = "Alda_Pacocha@hotmail.com"

    token: str = jwt_auth.generate_refresh_token(
        user_id=id_,
        name=name,
        email=email,
    )

    decoded_headers: dict[str, str] = jwt.get_unverified_header(token)
    decoded_payload: dict[str, str | int] | None = jwt_auth.get_token_payload(
        token=token,
        jwt_type="refresh",
    )

    assert decoded_payload
    assert "alg" in decoded_headers
    assert "typ" in decoded_headers
    assert decoded_headers["alg"] == test_settings.jwt.ALGORITHM
    assert decoded_headers["typ"] == "refresh"
    assert "sub" in decoded_payload
    assert "name" in decoded_payload
    assert "email" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert decoded_payload["sub"] == str(id_)
    assert decoded_payload["name"] == name
    assert decoded_payload["email"] == email
    assert decoded_payload["exp"] in range(
        int(decoded_payload["iat"]),
        int(decoded_payload["iat"])+test_settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS*24*60*61,
    )
    assert decoded_payload["iat"] in range(
        int(datetime.datetime.now(datetime.UTC).timestamp()),
        int(datetime.datetime.now(datetime.UTC).timestamp())+60,
    )


def test_get_token_payload_invalid_token() -> None:
    token: str = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiZW1haWwiOiJqZG9lQG1haWwudGxkIn0."
        "eyJleHAiOjE1MTYyMzkwMjJ9.7JvZ4"
    )

    payload: dict[str, str | int] | None = jwt_auth.get_token_payload(
        token=token,
        jwt_type="access",
    )

    assert payload is None


def test_get_token_payload_invalid_type() -> None:
    id_: int = 128903190823098
    name: str = "Ellen Purdy"
    email: str = "Edison47@yahoo.com"

    token: str = jwt_auth.generate_refresh_token(
        user_id=id_,
        name=name,
        email=email,
    )

    payload: dict[str, str | int] | None = jwt_auth.get_token_payload(
        token=token,
        jwt_type="access",
    )

    assert payload is None


def test_get_token_payload_invalid_signature() -> None:
    key: str = "mG?!a.Ab=_C5aiQ1eS5Z{r,@(jDFyC"*10
    now: int = int(datetime.datetime.now(datetime.UTC).timestamp())

    payload: dict[str, str | int] = {
        "sub": 1234561231227890,
        "name": "Lorenzo Swift",
        "email": "Garnet.Herman83@yahoo.com",
        "exp": now+24*60*60,
        "iat": now-24*60*60,
    }

    token: str = jwt.encode(
        payload,
        key,
        test_settings.jwt.ALGORITHM,
        headers={
            "typ": "access",
        },
    )

    decoded_payload: dict[str, str | int] | None = jwt_auth.get_token_payload(
        token=token,
        jwt_type="access",
    )

    assert decoded_payload is None


@pytest.mark.asyncio()
async def test_get_current_user(
    session: AsyncSession,
) -> None:

    name: str = "Miss Bill Wolff"
    email: str = "Daphne.Langosh@yahoo.com"
    password: str = "eKyoCKVuv8YJ8hR"

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
        access_token=HTTPAuthorizationCredentials(scheme="Bearer", credentials=token),
    )

    assert current_user
    assert current_user.id == user.id
    assert current_user.name == user.name
    assert current_user.email == user.email
    assert current_user.password != password
    assert current_user.is_password_valid(password)
    assert current_user.active == user.active


@pytest.mark.asyncio()
async def test_get_current_user_no_token(
    session: AsyncSession,
) -> None:

    with pytest.raises(ErrorException) as exc:
        await jwt_auth.get_current_user(
            session=session,
            access_token=None,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.response.get("errors", "") == []


@pytest.mark.asyncio()
async def test_get_current_user_no_user(
    session: AsyncSession,
) -> None:

    id_: int = 1234567890123498
    name: str = "Ms. Renee Goodwin"
    email: str = "Christina.Kuvalis@yahoo.com"

    token: str = jwt_auth.generate_access_token(
        user_id=id_,
        name=name,
        email=email,
    )

    with pytest.raises(ErrorException) as exc:
        await jwt_auth.get_current_user(
            session=session,
            access_token=HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials=token,
            ),
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.response.get("errors", "") == []


@pytest.mark.asyncio()
async def test_get_current_user_invalid_token(
    session: AsyncSession,
) -> None:

    name: str = "Ms. Renee Goodwin"
    email: str = "Christina.Kuvalis@yahoo.com"
    password: str = "ljrzf3_CHtFJobe"

    await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    with pytest.raises(ErrorException) as exc:
        await jwt_auth.get_current_user(
            session=session,
            access_token=HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials=f"{name*2}.{email*2}.{password*2}",
            ),
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.response.get("errors", "") == []


@pytest.mark.asyncio()
async def test_get_refreshed_user(
    session: AsyncSession,
) -> None:

    name: str = "Zella_Wehner69"
    email: str = "Gerhard52@gmail.com"
    password: str = "XSVFcSqsGhGpgor"

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    token: str = jwt_auth.generate_refresh_token(
        user_id=user.id,
        name=user.name,
        email=user.email,
    )

    current_user: User = await jwt_auth.get_refreshed_user(
        session=session,
        refresh_token=HTTPAuthorizationCredentials(scheme="Bearer", credentials=token),
    )

    assert current_user
    assert current_user.id == user.id
    assert current_user.name == user.name
    assert current_user.email == user.email
    assert current_user.password != password
    assert current_user.is_password_valid(password)
    assert current_user.active == user.active


@pytest.mark.asyncio()
async def test_get_refreshed_user_no_token(
    session: AsyncSession,
) -> None:

    with pytest.raises(ErrorException) as exc:
        await jwt_auth.get_refreshed_user(
            session=session,
            refresh_token=None,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.response.get("errors", "") == []


@pytest.mark.asyncio()
async def test_get_refreshed_user_no_user(
    session: AsyncSession,
) -> None:

    id_: int = 5187728381231
    name: str = "Mrs. Paul Moen"
    email: str = "Ettie94@gmail.com"

    token: str = jwt_auth.generate_refresh_token(
        user_id=id_,
        name=name,
        email=email,
    )

    with pytest.raises(ErrorException) as exc:
        await jwt_auth.get_refreshed_user(
            session=session,
            refresh_token=HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials=token,
            ),
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.response.get("errors", "") == []


@pytest.mark.asyncio()
async def test_get_refreshed_user_invalid_token(
    session: AsyncSession,
) -> None:

    name: str = "Terence Turner"
    email: str = "Leila.Monahan47@gmail.com"
    password: str = "6njYUvWPjfcG9Gs"

    await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    with pytest.raises(ErrorException) as exc:
        await jwt_auth.get_refreshed_user(
            session=session,
            refresh_token=HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials=f"{name*2}.{email*2}.{password*2}",
            ),
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.response.get("errors", "") == []
