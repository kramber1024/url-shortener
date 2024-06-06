from fastapi import APIRouter

from app.api.v1.main import api_router as v1_api_router

apis_router: APIRouter = APIRouter(prefix="/api")
apis_router.include_router(v1_api_router)
