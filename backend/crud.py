from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.models import User

if TYPE_CHECKING:
    from sqlalchemy.engine import Result


async def create_user(
    *,
    session: AsyncSession,
    name: str,
    email: str,
    password: str,
    salt_rounds: int = 15,
) -> User:

    user: User = User(
        name=name,
        email=email,
        password=password,
        salt_rounds=salt_rounds,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_email(
    *,
    session: AsyncSession,
    email: str,
) -> User | None:

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == email),
    )
    user: User | None = result.scalars().first()

    return user


async def get_user_by_id(
    *,
    session: AsyncSession,
    id_: int,
) -> User | None:

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.id == id_),
    )
    user: User | None = result.scalars().first()

    return user
