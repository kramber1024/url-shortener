import bcrypt
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "Users"

    name: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
    )
    password: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )
    banned: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
    )
    activated: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
    )

    def __init__(
        self,
        *,
        name: str,
        email: str,
        password: str,
        salt_rounds: int = 15,
    ) -> None:

        super().__init__()
        self.name = name
        self.email = self._format_email(email)
        self.password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(rounds=salt_rounds),
        ).decode()
        self.banned = False
        self.activated = False

    def is_password_valid(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.password.encode("utf-8"),
        )

    def _format_email(self, email: str) -> str:
        if "@" not in email:
            return email

        return f"{email.split("@")[0]}@{email.split('@')[1].lower()}"

    def __repr__(self) -> str:
        return f"<User {self.id} {self.name}>"
