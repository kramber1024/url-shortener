import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from backend.api import apis_router
from backend.api.v1.exceptions import ErrorException
from backend.api.v1.handlers import (
    error_exception_handler,
    server_error_exception_handler,
    validation_exception_handler,
)
from backend.core.database import db
from backend.views import router as views_router

app: FastAPI = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.include_router(apis_router)
app.include_router(views_router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ErrorException, error_exception_handler)
app.add_exception_handler(Exception, server_error_exception_handler)


async def main() -> None:
    await db.create_db(hard_rest=False)

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_includes=["*.html", "*.css", "*js"],
    )


if __name__ == "__main__":
    asyncio.run(main())
