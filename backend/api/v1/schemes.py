from typing import Annotated, Literal

from pydantic import BaseModel, EmailStr, Field

from backend.core.database.models import User as UserModel


class Error(BaseModel):
    message: Annotated[
        str,
        Field(
            description=(
                "Error message. "
                "Should not be used as feedback for a user."
            ),
            examples=["Password length is incorrect."],
        ),
    ]
    type: Annotated[
        str,
        Field(
            description=(
                "Error type. "
                "Should be used for frontend logic e.g. form validation."
            ),
            examples=["password"],
        ),
    ]


class ErrorResponse(BaseModel):
    errors: Annotated[
        list[Error],
        Field(
            description="List of errors.",
        ),
    ]
    message: Annotated[
        str,
        Field(
            description="Generic error message.",
            examples=["Validation error."],
        ),
    ]
    status: Annotated[
        int,
        Field(
            description="HTTP status code.",
            examples=[422],
            ge=100,
            le=599,
        ),
    ]


class SuccessResponse(BaseModel):
    message: Annotated[
        str,
        Field(
            description="Success message.",
            examples=["Operation completed successfully."],
        ),
    ]
    status: Annotated[
        int,
        Field(
            description="HTTP status code.",
            examples=[200],
            ge=100,
            le=599,
        ),
    ]


class UserRegistration(BaseModel):
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=32,
            description="Displayed in User's profile.",
            examples=["kramber"],
        ),
    ]
    email: Annotated[
        EmailStr,
        Field(
            min_length=len("*@*.*"),
            max_length=64,
            description="Used for authentication and notifications.",
            examples=["email@domain.tld"],
        ),
    ]
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=256,
            description="Used for authentication.",
            examples=["My$uper$ecretPa$$word"],
        ),
    ]
    terms: Annotated[
        Literal["on"],
        Field(
            description="User agreement to terms of use.",
            examples=["on"],
        ),
    ]


class UserLogin(BaseModel):
    email: Annotated[
        EmailStr,
        Field(
            min_length=len("*@*.*"),
            max_length=64,
            description="Email used for authentication.",
            examples=["email@domain.tld"],
        ),
    ]
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=256,
            description="Password used for authentication.",
            examples=["My$uper$ecretPa$$word"],
        ),
    ]


class User(BaseModel):
    id: Annotated[
        str,
        Field(
            description="Unique identifier for the user.",
            examples=["7205649978688008192"],
            max_length=len("7205649978688008192"),
            min_length=len("7205649978688008192"),
        ),
    ]
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=32,
            description="Displayed in profile.",
            examples=["kramber"],
        ),
    ]
    email: Annotated[
        EmailStr,
        Field(
            min_length=len("*@*.*"),
            max_length=64,
            description="Used for authentication.",
            examples=["email@domain.tld"],
        ),
    ]

    @classmethod
    def from_model(cls: type["User"], user: UserModel) -> "User":
        return cls(
            id=str(user.id),
            name=user.name,
            email=user.email,
        )
