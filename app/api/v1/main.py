from fastapi import APIRouter

from app.api.v1.routes import users

api_router: APIRouter = APIRouter(prefix="/v1")
api_router.include_router(users.router, tags=["Users"])
