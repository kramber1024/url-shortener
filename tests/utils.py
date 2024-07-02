from typing import Any

import bcrypt

SNOWFLAKE_RANGE: range = range(10**18, 10**19)
DB_USER_PASSWORD: str = "yK0jcTEZKd57NNf092a:1eb5:9148:44d6:077d:f71b:4936:0bb4"
DB_USER_PASSWORD_HASH: str = bcrypt.hashpw(
    DB_USER_PASSWORD.encode("utf-8"),
    bcrypt.gensalt(4),
).decode("utf-8")


def error_type_exists(json: dict[str, Any], error_type: str) -> bool:
    errors: list[dict[str, Any]] = json.get("errors", [])
    return any(error.get("type") == error_type for error in errors)


def format_email(email: str) -> str:
    if "@" not in email:
        return email
    email_splitted: list[str] = email.split("@")

    return f"{email_splitted[0]}@{email_splitted[1].lower()}"
