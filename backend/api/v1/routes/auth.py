from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend import crud
from backend.api.v1.exceptions import ErrorException
from backend.api.v1.schemes import ErrorResponse as ErrorResponseScheme
from backend.api.v1.schemes import SuccessResponse as SuccessResponseScheme
from backend.api.v1.schemes import UserLogin as UserLoginScheme
from backend.api.v1.schemes import UserRegistration as UserRegistrationScheme
from backend.core.auth import jwt_auth
from backend.core.configs import settings
from backend.core.database import db
from backend.core.database.models import User

router: APIRouter = APIRouter(prefix="/auth")


@router.post(
    "/register",
    summary="Register new user",
    description="Registers new user in the system.",
    status_code=201,
    responses={
        201: {
            "description": "New user registered successfully.",
            "model": SuccessResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "message": "User registered successfully.",
                        "status": 201,
                    },
                },
            },
        },
        409: {
            "description": (
                "The email is already in use. "
                "You should use a different email or send a request to /auth/login."
            ),
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [],
                        "message": "The email is already in use.",
                        "status": 409,
                    },
                },
            },
        },
        422: {
            "description": (
                "Validation error. "
                "The email format is invalid and/or the password length is incorrect "
                "(either too short or too long). Same goes for name field. "
                "Also you can get this error if "
                "you forgot to fill in the required fields."
            ),
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [
                            {
                                "message": "The name field is required.",
                                "type": "name",
                            },
                            {
                                "message": "The email format is invalid.",
                                "type": "email",
                            },
                            {
                                "message": "The password length is invalid.",
                                "type": "password",
                            },
                        ],
                        "message": "Validation error.",
                        "status": 422,
                    },
                },
            },
        },
    },
)
async def register_user(
    new_user: Annotated[
        UserRegistrationScheme,
        Body(),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db.scoped_session),
    ],
) -> JSONResponse:

    if await crud.get_user_by_email(
        session=session,
        email=new_user.email,
    ) is not None:
        raise ErrorException(
            errors=[],
            message="The email is already in use.",
            status=status.HTTP_409_CONFLICT,
        )

    await crud.create_user(
        session=session,
        name=new_user.name,
        email=new_user.email,
        password=new_user.password,
    )

    success_response: SuccessResponseScheme = SuccessResponseScheme(
        message="User registered successfully.",
        status=status.HTTP_201_CREATED,
    )

    return JSONResponse(
        content=success_response.model_dump(),
        status_code=status.HTTP_201_CREATED,
    )


@router.post(
    "/login",
    summary="Authenticate user",
    description="Authenticates a user in the system using email and password.",
    status_code=200,
    responses={
        200: {
            "description": "User authenticated successfully.",
            "model": SuccessResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "message": "User authenticated successfully.",
                        "status": 200,
                    },
                },
            },
        },
        401: {
            "description": "The email or password is incorrect.",
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [],
                        "message": "The email or password is incorrect.",
                        "status": 401,
                    },
                },
            },
        },
        422: {
            "description": (
                "Validation error. "
                "The email format is invalid and/or the password length is incorrect "
                "(either too short or too long). "
                "Also you can get this error if "
                "you forgot to fill in the required fields."
            ),
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                          "errors": [
                                {
                                    "message": "The email field is required.",
                                    "type": "email",
                                },
                                {
                                    "message": "The password length is invalid.",
                                    "type": "password",
                                },
                            ],
                            "message": "Validation error.",
                            "status": 422,
                    },
                },
            },
        },
    },
)
async def authenticate_user(
    user_credentials: Annotated[
        UserLoginScheme,
        Body(),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db.scoped_session),
    ],
) -> JSONResponse:

    user: User | None = await crud.get_user_by_email(
        session=session,
        email=user_credentials.email,
    )

    if user is None or not user.is_password_valid(user_credentials.password):
        raise ErrorException(
            errors=[],
            message="The email or password is incorrect.",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    access_token: str = jwt_auth.generate_access_token(user.id, user.name, user.email)
    refresh_token: str = jwt_auth.generate_refresh_token(user.id, user.name, user.email)

    success_response: SuccessResponseScheme = SuccessResponseScheme(
        message="User authenticated successfully.",
        status=status.HTTP_200_OK,
    )

    response: JSONResponse = JSONResponse(
        content=success_response.model_dump(),
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,
        httponly=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        secure=True,
        httponly=True,
    )

    return response


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Refreshes the access token using the refresh token.",
    status_code=200,
    responses={
        200: {
            "description": "Tokens refreshed successfully.",
            "model": SuccessResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "message": "Tokens refreshed successfully.",
                        "status": 200,
                    },
                },
            },
        },
        400: {
            "description": "Provided token is not valid.",
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [],
                        "message": "Invalid token.",
                        "status": 400,
                    },
                },
            },
        },
        401: {
            "description": "Authorization required. Provide a valid token in headers.",
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [],
                        "message": "Authorization required.",
                        "status": 401,
                    },
                },
            },
        },
        422: {
            "description": "Provided token is not valid.",
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [],
                        "message": "Invalid token.",
                        "status": 400,
                    },
                },
            },
        },
    },
)
async def refresh_user(
    user: Annotated[
        User,
        Depends(jwt_auth.get_refreshed_user),
    ],
) -> JSONResponse:

    access_token: str = jwt_auth.generate_access_token(user.id, user.name, user.email)
    refresh_token: str = jwt_auth.generate_refresh_token(user.id, user.name, user.email)

    success_response: SuccessResponseScheme = SuccessResponseScheme(
        message="Tokens refreshed successfully.",
        status=status.HTTP_200_OK,
    )

    response: JSONResponse = JSONResponse(
        content=success_response.model_dump(),
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,
        httponly=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        secure=True,
        httponly=True,
    )

    return response
