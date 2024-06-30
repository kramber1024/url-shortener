import bcrypt
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "Users"

    first_name: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
    )
    last_name: Mapped[str | None] = mapped_column(
        String(16),
        nullable=True,
    )
    email: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
    )
    phone: Mapped[str | None] = mapped_column(
        String(16),
        nullable=True,
    )
    password: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    def __init__(
        self,
        *,
        first_name: str,
        last_name: str | None,
        email: str,
        password: str,
    ) -> None:

        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = None
        self.password = password

    def is_password_valid(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.password.encode("utf-8"),
        )

    def __repr__(self) -> str:
        return f"<User {self.id}>"
