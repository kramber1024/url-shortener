from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.database.generator import gen


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        unique=True,
        sort_order=-1,
    )

    def __init__(self) -> None:
        self.id = gen.id
