from app.core.database.models import User
from app.tests.utils.utils import random_email, random_string_of_random_length


def random_user_credentials() -> tuple[str, str, str]:
    return (
        random_string_of_random_length(1, User.name.type.length),
        random_email(User.email.type.length),
        random_string_of_random_length(8, User.password.type.length),
    )
