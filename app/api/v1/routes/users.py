from fastapi import APIRouter

from app.api.v1.dependencies import SessionDependency
from app.api.v1.schemes import User as UserResponse

router: APIRouter = APIRouter(prefix="/users")


@router.get(
    "/me",
    summary="Get current user",
    description="Get information about the current user",
    response_model=UserResponse,
    responses={
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "name": "Oleg",
                        "avatar": "https://avatars.githubusercontent.com/u/26481850?v=4",
                    },
                },
            },
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User not found",
                    },
                },
            },
        },
    },
)
async def read_users_me(session: SessionDependency) -> dict[str, str]:
    return {"a": "a"}
