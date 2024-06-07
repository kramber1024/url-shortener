from fastapi import APIRouter

from .routes import auth, users

api_router: APIRouter = APIRouter(prefix="/v1")
api_router.include_router(users.router, tags=["Users"])
api_router.include_router(auth.router, tags=["Auth"])
