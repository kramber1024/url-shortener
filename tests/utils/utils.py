import secrets
import string


def random_string(
    length: int = 8,
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


def random_email(
    max_length: int = 64,
) -> str:

    max_length -= 5 # @.tld

    return (
        f"{random_string_of_random_length(1, max_length // 2)}"
        f"@{random_string_of_random_length(1, max_length // 2)}"
        f".{random_string_of_random_length(2, 3)}"
    )


def format_email(email: str) -> str:
    return email.split("@")[0] + "@" + email.split("@")[1].lower()


def random_id() -> int:
    return secrets.randbelow(10**19 - 10**18) + 10**18
