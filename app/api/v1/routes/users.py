from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemes import ErrorResponse as ErrorResponseScheme
from app.api.v1.schemes import User as UserScheme
from app.core.database.models import User
from app.core.utils import jwt_auth

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
    # TODO(kramber): Add scheme for successful response.
    # 001
    responses={},
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
