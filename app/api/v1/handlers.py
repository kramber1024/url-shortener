from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.schemes import Error as ErrorScheme
from app.api.v1.schemes import ErrorResponse as ErrorResponseScheme


async def validation_exception_handler(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:

    errors_map: dict[str, str] = {
        "string_too_short": "The {} length is invalid.",
        "string_too_long": "The {} length is invalid.",
        "value_error": "The {} format is invalid.",
        "missing": "The {} field is required.",
        "string_type": "The {} should be a string.",
    }

    errors: list[ErrorScheme] = []
    for error in exc.errors():
        message: str = errors_map.get(
            error["type"],
            f"Invalid value ({error["type"]}).",
        ).format(error["loc"][1])

        errors.append(
            ErrorScheme(
                message=message,
                type=error["loc"][1],
            ),
        )

    response: ErrorResponseScheme = ErrorResponseScheme(
        errors=errors,
        message="Validation error.",
        status=422,
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response.model_dump(),
    )