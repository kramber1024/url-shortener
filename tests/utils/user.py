from app.core.database.models import User
from tests.utils.utils import random_email, random_string_of_random_length


def random_user_credentials() -> tuple[str, str, str]:
    """Generate random user credentials.

    Returns
    -------
        A tuple containing three strings: a random name, a random email,
        and a random password.

    """
    return (
        random_string_of_random_length(1, User.name.type.length),
        random_email(User.email.type.length),
        random_string_of_random_length(8, User.password.type.length),
    )