from typing import TYPE_CHECKING

import bcrypt
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .bases import IDBase

if TYPE_CHECKING:
    from .status import Status


class User(IDBase):
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

    status: Mapped["Status"] = relationship("Status", lazy="selectin")

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

    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name or ""}".strip()

    def is_password_valid(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.password.encode("utf-8"),
        )

    def __repr__(self) -> str:
        return f"<User {self.id}>"
