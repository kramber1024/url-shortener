from datetime import datetime
from typing import TYPE_CHECKING, Literal

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Verification(Base):
    __tablename__ = "Verifications"

    user_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey("Users.id"),
        nullable=False,
    )
    type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )
    secret: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )
    expiration: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User")

    def __init__(
        self,
        *,
        user_id: int,
        type_: Literal["email"],
        secret: str,
        expiration: datetime,
    ) -> None:

        super().__init__()
        self.user_id = user_id
        self.type = type_
        self.secret = secret
        self.expiration = expiration
