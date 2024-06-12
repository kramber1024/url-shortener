from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse

from app import crud
from app.api.v1.dependencies import SessionDependence
from app.api.v1.exceptions import ErrorException
from app.api.v1.schemes import ErrorResponse as ErrorResponseScheme
from app.api.v1.schemes import User as UserScheme
from app.api.v1.schemes import UserLogin as UserLoginScheme
from app.api.v1.schemes import UserRegistration as UserRegistrationScheme

if TYPE_CHECKING:
    from app.core.database.models import User

router: APIRouter = APIRouter(prefix="/auth")


@router.post(
    "/register",
    summary="Register new user",
    description="Registers new user in the system.",
    status_code=201,
    responses={
        # TODO(kramber): Add real response for 201. Change 'model' and 'example'.
        # 001
        201: {
            "description": "New user registered successfully.",
            "model": UserScheme,
            "content": {
                "application/json": {
                    "example": {
                        "PLACEHOLDER": "PLACEHOLDER",
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
    new_user: Annotated[UserRegistrationScheme, Body],
    session: SessionDependence,
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

    user: User = await crud.create_user(
        session=session,
        name=new_user.name,
        email=new_user.email,
        password=new_user.password,
    )

    return JSONResponse(
        content=UserScheme.from_model(user).model_dump(),
        status_code=status.HTTP_201_CREATED,
    )


@router.post(
    "/login",
    summary="Authenticate user",
    description="Authenticates a user in the system using email and password.",
    status_code=200,
    responses={
        # TODO(kramber): Add real response for 201. Change 'model' and 'example'.
        # 001
        201: {
            "description": "New user registered successfully.",
            "model": UserScheme,
            "content": {
                "application/json": {
                    "example": {
                        "PLACEHOLDER": "PLACEHOLDER",
                    },
                },
            },
        },
        401: {
            "description": "New user registered successfully.",
            "model": UserScheme,
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
                "(either too short or too long). Same goes for name field. "
                "Also you can get this error if "
                "you forgot to fill in the required fields."
            ),
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "PLACEHOLDER": "PLACEHOLDER",
                    },
                },
            },
        },
    },
)
async def authenticate_user(
    user_credentials: Annotated[UserLoginScheme, Body],
    session: SessionDependence,
) -> JSONResponse:

    user: User | None = await crud.get_user_by_email(
        session=session,
        email=user_credentials.email,
    )

    if user is None:
        raise ErrorException(
            errors=[],
            message="The email or password is incorrect.",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_password_valid(user_credentials.password):
        raise ErrorException(
            errors=[],
            message="The email or password is incorrect.",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return JSONResponse(
        content=UserScheme.from_model(user).model_dump(),
        status_code=status.HTTP_200_OK,
    )
