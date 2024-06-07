import asyncio

import uvicorn
from fastapi import FastAPI

from app.api import apis_router
from app.core.database import db

app: FastAPI = FastAPI()
app.include_router(apis_router)


async def main() -> None:
    await db.create_db(hard_rest=False)

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
