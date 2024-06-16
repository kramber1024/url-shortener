import datetime
from typing import Literal

import jwt
import pytest

from app.core.auth import jwt_auth
from app.core.configs import test_settings


@pytest.mark.parametrize(
    ("jwt_type", "payload"),
    [
        (
            "access",
            {
                "sub": 7207503858480705536,
                "name": "Fuleat",
                "email": "HarryByrne@teleworm.us",
                "key": "Newmark & Lewis",
            },
        ),
        (
            "access",
            {
                "sub": 7207503858480705536,
                "name": "123123",
                "email": "55.628354, 12.636962",
                "key": "198.4 pounds (90.2 kilograms)",
            },
        ),
        (
            "refresh",
            {
                "sub": -1000000000,
                "name": "True",
                "email": "Mozilla/5.0@...........",
                "key": "21f323d3-6df2-4d27-994a-6ec0af48ad50",
            },
        ),
        (
            "refresh",
            {
                "sub": -0,
                "name": 123123,
                "email": "28 years old",
                "key": "July 12, 1995",
            },
        ),
        (
            "refresh",
            {
                "sub": 0,
                "name": "",
                "email": "",
                "key": "",
            },
        ),
    ],
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
