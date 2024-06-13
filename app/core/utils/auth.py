import datetime
from typing import Literal

import jwt

from app.core.config import settings


def _encode_jwt(
    jwt_type: Literal["access", "refresh"],
    payload: dict[str, str | int],
    key: str = settings.jwt.SECRET,
    algorithm: str = settings.jwt.ALGORITHM,
) -> str:

    now: int = int(datetime.datetime.now(datetime.UTC).timestamp())

    if jwt_type == "access":
        expire: int = now + settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    else:
        expire = now + settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60

    payload.update(
        {
            "exp": expire,
            "iat": now,
        },
    )
    return jwt.encode(
        payload,
        key,
        algorithm,
        headers={
            "typ": jwt_type,
        },
    )


def generate_access_token(
    user_id: int,
    name: str,
    email: str,
) -> str:

    return _encode_jwt(
        jwt_type="access",
        payload={
            "sub": str(user_id),
            "name": name,
            "email": email,
        },
    )


def generate_refresh_token(
    user_id: int,
    name: str,
    email: str,
) -> str:

    return _encode_jwt(
        jwt_type="refresh",
        payload={
            "sub": str(user_id),
            "name": name,
            "email": email,
        },
    )
