import datetime
import secrets
from typing import Literal

import jwt
import pytest

from app.core.auth import jwt_auth
from app.core.config import settings
from app.tests import utils


@pytest.mark.parametrize(
    "jwt_type", [
        "access",
        "refresh",
    ],
)
def test__encode_jwt(
    jwt_type: Literal["access", "refresh"],
) -> None:
    random_key_1: str = utils.random_string(16)
    random_key_2: str = utils.random_string(16)
    random_key_3: str = utils.random_string(16)

    payload: dict[str, str | int] = {
        "sub": utils.random_string(19),
        "name": utils.random_string_of_random_length(8, 32),
        "email": utils.random_email(max_length=64),
        random_key_1: utils.random_string_of_random_length(8, 32),
        random_key_2: utils.random_string_of_random_length(8, 32),
        random_key_3: utils.random_string_of_random_length(8, 32),
    }

    token: str = jwt_auth._encode_jwt(
        jwt_type=jwt_type,
        payload=payload,
    )

    decoded_payload: dict[str, str | int] = jwt.decode(
        token,
        key=settings.jwt.SECRET,
        algorithms=[settings.jwt.ALGORITHM],
    )

    assert "sub" in decoded_payload
    assert "name" in decoded_payload
    assert "email" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert random_key_1 in decoded_payload
    assert random_key_2 in decoded_payload
    assert random_key_3 in decoded_payload
    assert decoded_payload["sub"] == payload["sub"]
    assert decoded_payload["name"] == payload["name"]
    assert decoded_payload["email"] == payload["email"]
    assert isinstance(decoded_payload["exp"], int)
    assert isinstance(decoded_payload["iat"], int)
    assert decoded_payload[random_key_1] == payload[random_key_1]
    assert decoded_payload[random_key_2] == payload[random_key_2]
    assert decoded_payload[random_key_3] == payload[random_key_3]


def test_generate_access_token() -> None:
    user_id: int = utils.random_id()
    name, email, _ = utils.random_user_credentials()

    token: str = jwt_auth.generate_access_token(
        user_id=user_id,
        name=name,
        email=email,
    )

    decoded_headers: dict[str, str] = jwt.get_unverified_header(token)
    decoded_payload: dict[str, str | int] = jwt.decode(
        token,
        key=settings.jwt.SECRET,
        algorithms=[settings.jwt.ALGORITHM],
    )

    # Headers
    assert "alg" in decoded_headers
    assert "typ" in decoded_headers
    assert decoded_headers["alg"] == settings.jwt.ALGORITHM
    assert decoded_headers["typ"] == "access"
    # Payload
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


def test_generate_refresh_token() -> None:
    user_id: int = utils.random_id()
    name, email, _ = utils.random_user_credentials()

    token: str = jwt_auth.generate_refresh_token(
        user_id=user_id,
        name=name,
        email=email,
    )

    decoded_headers: dict[str, str] = jwt.get_unverified_header(token)
    decoded_payload: dict[str, str | int] = jwt.decode(
        token,
        key=settings.jwt.SECRET,
        algorithms=[settings.jwt.ALGORITHM],
    )

    # Headers
    assert "alg" in decoded_headers
    assert "typ" in decoded_headers
    assert decoded_headers["alg"] == settings.jwt.ALGORITHM
    assert decoded_headers["typ"] == "refresh"
    # Payload
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
    "jwt_type", [
        "access",
        "refresh",
    ],
)
def test_get_token_payload(
    jwt_type: Literal["access", "refresh"],
) -> None:
    user_id = utils.random_id()
    name, email, _ = utils.random_user_credentials()

    if jwt_type == "access":
        token: str = jwt_auth.generate_access_token(
            user_id=user_id,
            name=name,
            email=email,
        )
    else:
        token = jwt_auth.generate_refresh_token(
            user_id=user_id,
            name=name,
            email=email,
        )

    headers: dict[str, str] = jwt.get_unverified_header(token)
    payload: dict[str, str | int] | None = jwt_auth.get_token_payload(
        token=token,
        jwt_type=jwt_type,
    )

    assert payload is not None
    # Headers
    assert "alg" in headers
    assert "typ" in headers
    assert headers["alg"] == settings.jwt.ALGORITHM
    assert headers["typ"] == jwt_type
    # Payload
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
    "token", [
        "",
        utils.random_string_of_random_length(256, 512),
        utils.random_string_of_random_length(128, 256),
        (
            f"{utils.random_string_of_random_length(64, 128)}."
            f"{utils.random_string_of_random_length(64, 128)}."
            f"{utils.random_string_of_random_length(64, 128)}"
        ),
        "...",
        "a.a.a",
        str(utils.random_id()),
    ],
)
def test_get_token_payload_invalid_token(
    token: str,
) -> None:
    jwt_type: Literal["access", "refresh"] = secrets.choice(["access", "refresh"])

    payload: dict[str, str | int] | None = jwt_auth.get_token_payload(
        token=token,
        jwt_type=jwt_type,
    )

    assert payload is None


@pytest.mark.parametrize(
    ("key", "jwt_type"), [
        ("", "access"),
        ("", "refresh"),
        (utils.random_string(16), "access"),
        (utils.random_string(16), "refresh"),
        (utils.random_string(32), "access"),
        (utils.random_string(32), "refresh"),
        (utils.random_string(64), "access"),
        (utils.random_string(64), "refresh"),
    ],
)
def test_get_token_payload_invalid_signature(
    key: str,
    jwt_type: Literal["access", "refresh"],
) -> None:
    user_id = utils.random_id()
    name, email, _ = utils.random_user_credentials()
    now: int = int(datetime.datetime.now(datetime.UTC).timestamp())

    payload: dict[str, str | int] = {
        "sub": str(user_id),
        "name": name,
        "email": email,
        "exp": now+24*60*60,
        "iat": now-24*60*60,
    }

    token: str = jwt.encode(
        payload,
        key,
        settings.jwt.ALGORITHM,
        headers={
            "typ": jwt_type,
        },
    )

    decoded_payload: dict[str, str | int] | None = jwt_auth.get_token_payload(
        token=token,
        jwt_type=jwt_type,
    )

    assert decoded_payload is None

# TODO(kramber): Add test for get_current_user dependency
# 001
