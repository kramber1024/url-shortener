from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr


class Error(BaseModel):
    message: str
    type: str


class ErrorResponse(BaseModel):
    errors: list[Error]
    message: str
    status: int


class UserRegistration(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(128)]


class User(BaseModel):
    id: str
    name: str
    avatar: str
