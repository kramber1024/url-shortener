from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from tests import utils

if TYPE_CHECKING:
    from app.core.database.models import User


class TestCRUDUser:
    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("name", "email", "password"),
        [
            ("John", "JOHN@EMAIL.TLD", "password"),
            ("JussiSeikola", "JussiSeikola@MyMaIl.co", "!#$%&'()*,./:;<=>?@[]^_`{|}~"),
            ("Лайма Назарова", "YetererCOOLDomain.com", "'''''''%$#@#!123123zxc///\\"),
            ("", "", ""),
            ("W"*32, "X"*64, "E"*256),
        ],
    )
    async def test_create_user(
        self,
        session: AsyncSession,
        name: str,
        email: str,
        password: str,
    ) -> None:

        user: User = await crud.create_user(
            session=session,
            name=name,
            email=email,
            password=password,
        )

        assert user is not None
        assert isinstance(user.id, int)
        assert user.name == name
        assert user.email == utils.format_email(email)
        assert user.password != password
        assert user.is_password_valid(password)
        assert user.active

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("name", "email", "password"),
        [
            ("Valérie Dodier", "ValerieDodier@daYSrep.cOm", "Aingo2ShAingo2Sh5123"),
            ("Chyou Mao", "ChyouMao@Extraville.fi", "!#$%&'()*,./:;<=>?@[]^_`{|}~"),
            (
                "Larissa Fernandes Barros",
                "LarissaFernandesBarros@josagafffrapide.com",
                "'''''''%$#@#!123123c///\\"*8,
            ),
            ("", "", ""),
            ("1"*32, "2"*64, "3"*256),
        ],
    )
    async def test_get_user_by_email(
        self,
        session: AsyncSession,
        name: str,
        email: str,
        password: str,
    ) -> None:

        user: User = await crud.create_user(
            session=session,
            name=name,
            email=email,
            password=password,
        )

        found_user: User | None = await crud.get_user_by_email(
            session=session,
            email=utils.format_email(email),
        )

        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.name == user.name
        assert found_user.email == user.email
        assert found_user.password != password
        assert found_user.is_password_valid(password)
        assert found_user.active == user.active


    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("name", "email", "password"),
        [
            ("Sienna Jackson", "ValerieDodier@daYSrep.cOm", "Aingo2ShAingo2Sh5123"),
        ],
    )
    async def test_get_user_by_email_not_found(
        self,
        session: AsyncSession,
        name: str,
        email: str,
        password: str,
    ) -> None:

        await crud.create_user(
            session=session,
            name=name,
            email=email,
            password=password,
        )

        found_user: User | None = await crud.get_user_by_email(
            session=session,
            email=email + ";",
        )

        assert found_user is None


    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("name", "email", "password"),
        [
            ("Tyler Reid", "Ty-.id@ASD.com", "388983c6-f14f-4d19-b661-cb192fdc47da"),
            ("Hosseed", "TeganAkhtar@Gmail.com", "eL0rithoo"),
            ("Tegan Akhtar", "GracieWallismail.ru", "!#$%&'()*,./:;<=>?@[]^_`{|}~"),
            ("", "", ""),
            ("!"*32, "^"*64, "@"*256),
        ],
    )
    async def test_get_user_by_id(
        self,
        session: AsyncSession,
        name: str,
        email: str,
        password: str,
    ) -> None:

        user: User = await crud.create_user(
            session=session,
            name=name,
            email=email,
            password=password,
        )

        found_user: User | None = await crud.get_user_by_id(
            session=session,
            _id=user.id,
        )

        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.name == user.name
        assert found_user.email == user.email
        assert found_user.password != password
        assert found_user.is_password_valid(password)
        assert found_user.active == user.active

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("name", "email", "password"),
        [
            ("Άγιος Γεώργιος", "SpencerCameron@Bitterephe.Yu", "1Z 2F4 451 53 6378"),
        ],
    )
    async def test_get_user_by_id_not_found(
        self,
        session: AsyncSession,
        name: str,
        email: str,
        password: str,
    ) -> None:

        user: User = await crud.create_user(
            session=session,
            name=name,
            email=email,
            password=password,
        )

        found_user: User | None = await crud.get_user_by_id(
            session=session,
            _id=user.id-1,
        )

        assert found_user is None
