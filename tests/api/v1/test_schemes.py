from app.api.v1.schemes import User as UserScheme
from app.core.database.models import User as UserModel


def test_user_scheme() -> None:
    name: str = "Dillon.Howe"
    email: str = "Dovie87@gmail.com"
    password: str = "YzbXhViCSId_pJK"

    user_model: UserModel = UserModel(
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )
    user_scheme: UserScheme = UserScheme.from_model(user_model)

    assert isinstance(user_scheme, UserScheme)
    assert user_scheme.id == str(user_model.id)
    assert user_scheme.name == user_model.name
    assert user_scheme.email == user_model.email

