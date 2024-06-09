from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "Users"

    name: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)

    def __init__(self, *, name: str, email: str, password: str) -> None:
        super().__init__()
        self.name = name
        self.email = email
        self.password = hashpw(password.encode("utf-8"), gensalt(rounds=15)).decode()

    def __repr__(self) -> str:
        return f"<User {self.id} {self.name}>"

    def is_password_valid(self, password: str) -> bool:
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
