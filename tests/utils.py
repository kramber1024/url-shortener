from typing import Any


def error_type_exists(json: dict[str, Any], error_type: str) -> bool:
    errors: list[dict[str, Any]] = json.get("errors", [])
    return any(error.get("type") == error_type for error in errors)


def format_email(email: str) -> str:
    return email.split("@")[0] \
        + f"@{email.split("@")[1].lower()}" if "@" in email else ""
