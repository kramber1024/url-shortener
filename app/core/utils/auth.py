import jwt

from app.core.config import settings


def encode_jwt(
    data: dict,
    secret: str,
    algorithm: str = settings.
) -> str:

    return jwt.encode(data, secret, algorithm=algorithm)