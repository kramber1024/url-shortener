from app.core.database.models import User
from app.tests.utils.utils import random_email, random_string_of_random_length


def random_user() -> User:
    return User(
        name=random_string_of_random_length(1, User.name.type.length),
        email=random_email(max_length=User.email.type.length),
        password=random_string_of_random_length(8, User.password.type.length),
    )
