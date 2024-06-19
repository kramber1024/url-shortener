import datetime
from typing import Annotated, Literal

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.configs import settings
from app.core.database import db
from app.core.database.models import User

http_bearer: HTTPBearer = HTTPBearer(
    auto_error=False,
)

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


def get_token_payload(
    token: str,
    jwt_type: Literal["access", "refresh"],
) -> dict[str, str | int] | None:
    """Get payload from a JWT token.

    Args:
    ----
        token: The JWT token.
        jwt_type: The type of JWT token. Either "access" or "refresh".

    Returns:
    -------
        dict[str, str | int] | None: The payload of the JWT token if the
        token type matches and signature is valid, otherwise None.

    Raises:
    ------
        None

    Example:
    -------
        >>> token = "eyJhbGciOiJIUzasdasd5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwib\
        FtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNasdasdyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        >>> jwt_type = "access"
        >>> get_token_payload(token, jwt_type)
        {'sub': '1234567890', 'name': 'John Doe', 'iat': 1516239022}

    """
    try:
        if jwt.get_unverified_header(token).get("typ", "") != jwt_type:
            return None

        token_payload: dict[str, str | int] = jwt.decode(
            token,
            settings.jwt.SECRET,
            algorithms=[settings.jwt.ALGORITHM],
            options={
                "require": [
                    "sub",
                    "name",
                    "email",
                    "exp",
                    "iat",
                ],
                "verify_exp": True,
                "verify_signature": True,
            },
        )

    except jwt.InvalidTokenError:
        return None

    return token_payload


async def get_current_user(
    session: Annotated[
        AsyncSession,
        Depends(db.scoped_session),
    ],
    token: Annotated[
        HTTPAuthorizationCredentials,
        Depends(http_bearer),
    ],
) -> User:
    from app.api.v1.exceptions import ErrorException

    if token is None:
        raise ErrorException(
            errors=[],
            message="Authorization required.",
            status=401,
        )

    payload: dict[str, str | int] | None = get_token_payload(
        token.credentials,
        jwt_type="access",
    )

    if payload is None:
        raise ErrorException(
            errors=[],
            message="Invalid token.",
            status=400,
        )

    user: User | None = await crud.get_user_by_id(
        session=session,
        id_=int(payload.get("sub", -1)),
    )

    if user is None:
        raise ErrorException(
            errors=[],
            message="Invalid token.",
            status=400,
        )

    return user
