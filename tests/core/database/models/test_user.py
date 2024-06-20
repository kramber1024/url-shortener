from app.core.database.models import User


def test_user_repr() -> None:
    name: str = "Doris Shields"
    email: str = "Bernard.Dooley@gmail.com"
    password: str = "sVn1C73Bkmreeyi"

    user: User = User(
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    assert user.__repr__() == f"<User {user.id} {user.name}>"
