import secrets
import string


def random_string(
    length: int,
    *,
    include_uppercase: bool = True,
) -> str:

    length = 1 if length < 1 else length

    alphabet = string.ascii_lowercase

    if include_uppercase:
        alphabet += string.ascii_uppercase

    return "".join(secrets.choice(alphabet) for _ in range(length))


def random_string_of_random_length(
    min_length: int = 8,
    max_length: int = 32,
    *,
    include_uppercase: bool = True,
) -> str:

    length: int = secrets.randbelow(max_length - min_length + 1) + min_length # [n, m]
    return random_string(length, include_uppercase=include_uppercase)


def random_email() -> str:
    return (
        f"{random_string_of_random_length(1, 20)}"
        f"@{random_string_of_random_length(1, 20)}"
        f".{random_string_of_random_length(2, 3, include_uppercase=False)}"
    )


