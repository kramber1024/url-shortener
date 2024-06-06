import uvicorn
from fastapi import FastAPI

from app.api import apis_router

app: FastAPI = FastAPI()
app.include_router(apis_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
