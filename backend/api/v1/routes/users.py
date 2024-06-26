from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from backend.api.v1.schemes import ErrorResponse as ErrorResponseScheme
from backend.api.v1.schemes import User as UserScheme
from backend.core.auth import jwt_auth
from backend.core.database.models import User

router: APIRouter = APIRouter(
    prefix="/users",
    responses={
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
    },
)


@router.get(
    "/me",
    summary="Get current user",
    description="Get information about the current user",
    responses={
        200: {
            "description": "User information retrieved successfully.",
            "model": UserScheme,
            "content": {
                "application/json": {
                    "example": {
                        "id": "7207306656936357888",
                        "name": "kramber",
                        "email": "email@domain.tld",
                    },
                },
            },
        },
    },
)
async def get_users_me(
    user: Annotated[
        User,
        Depends(jwt_auth.get_current_user),
    ],
) -> JSONResponse:

    return JSONResponse(
        content=UserScheme.from_model(user).model_dump(),
        status_code=status.HTTP_200_OK,
    )
