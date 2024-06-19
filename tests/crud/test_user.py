import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database.models import User
from tests import utils


@pytest.mark.asyncio()
async def test_create_user(
    session: AsyncSession,
) -> None:

    name: str = "Test User"
    email: str = "test@mail.tld"
    password: str = "testpassword"

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    assert user
    assert isinstance(user, User)
    assert isinstance(user.id, int)
    assert user.name == name
    assert user.email == email
    assert user.password != password
    assert user.is_password_valid(password)
    assert user.active


@pytest.mark.asyncio()
async def test_create_user_uppercase(
    session: AsyncSession,
) -> None:

    name: str = "TEST USER"
    email: str = "TEST@EMAIL.TLD"
    password: str = "TESTPASSWORD"

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    assert user
    assert isinstance(user, User)
    assert isinstance(user.id, int)
    assert user.name == name
    assert user.email == utils.format_email(email)
    assert user.password != password
    assert user.is_password_valid(password)
    assert user.active


@pytest.mark.asyncio()
async def test_create_user_empty(
    session: AsyncSession,
) -> None:

    name: str = ""
    email: str = ""
    password: str = ""

    user: User = await crud.create_user(
        session=session,
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    assert user
    assert isinstance(user, User)
    assert isinstance(user.id, int)
    assert user.name == name
    assert user.email == email
    assert user.password != password
    assert user.is_password_valid(password)
    assert user.active


@pytest.mark.asyncio()
async def test_get_user_by_email(
    session: AsyncSession,
) -> None:

    name: str = "Test User"
    email: str = "test@mail.tld"
    password: str = "testpassword"

    session.add(
        User(
            name=name,
            email=email,
            password=password,
            salt_rounds=4,
        ),
    )
    await session.commit()

    found_user: User | None = await crud.get_user_by_email(
        session=session,
        email=email,
    )

    assert found_user
    assert isinstance(found_user, User)
    assert isinstance(found_user.id, int)
    assert found_user.name == name
    assert found_user.email == email
    assert found_user.password != password
    assert found_user.is_password_valid(password)
    assert found_user.active


@pytest.mark.asyncio()
async def test_get_user_by_email_not_found(
    session: AsyncSession,
) -> None:

    name: str = "Test User"
    email: str = "test@mail.tld"
    password: str = "testpassword"

    session.add(
        User(
            name=name,
            email=email,
            password=password,
            salt_rounds=4,
        ),
    )
    await session.commit()

    found_user: User | None = await crud.get_user_by_email(
        session=session,
        email=email[::-1],
    )

    assert found_user is None


@pytest.mark.asyncio()
async def test_get_user_by_id(
    session: AsyncSession,
) -> None:

    name: str = "Test User"
    email: str = "test@mail.tld"
    password: str = "testpassword"

    user: User = User(
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    found_user: User | None = await crud.get_user_by_id(
        session=session,
        id_=user.id,
    )

    assert found_user
    assert isinstance(found_user, User)
    assert found_user.id == user.id
    assert found_user.name == name
    assert found_user.email == email
    assert found_user.password != password
    assert found_user.is_password_valid(password)
    assert found_user.active


@pytest.mark.asyncio()
async def test_get_user_by_id_not_found(
    session: AsyncSession,
) -> None:

    name: str = "Test User"
    email: str = "test@mail.tld"
    password: str = "testpassword"

    user: User = User(
        name=name,
        email=email,
        password=password,
        salt_rounds=4,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    found_user: User | None = await crud.get_user_by_id(
        session=session,
        id_=user.id - 1,
    )

    assert found_user is None
