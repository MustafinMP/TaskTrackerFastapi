from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from exceptions.user_exceptions import UserIsAlreadyExistsError
from infrastructure.db_models.user_models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_by_id(self, user_id: int) -> User | None:
        """Find user in database by id.

        :param user_id: the id of the user.
        :return: user object or none.
        """

        stmt = select(User).where(User.id == user_id).options(joinedload(User.teams))
        return await self.session.scalar(stmt)

    async def get_by_email(self, user_email: str) -> User | None:
        """Find user in database by email.

        :param user_email: the email of the user.
        :return: user object or none.
        """

        stmt = select(User).where(User.email == user_email)
        return await self.session.scalar(stmt)

    async def get_by_yandex_id(self, yandex_id: int) -> User | None:
        """Find user in database by id.

        :param yandex_id: the yandex oauth id of the user.
        :return: user object or none.
        """

        stmt = select(User).where(User.oauth_yandex_id == yandex_id).options(joinedload(User.teams))
        return await self.session.scalar(stmt)

    async def add(self, name: str, email: str, password: str) -> int:
        """Create new user by data from register form.

        :param name:
        :param email:
        :param password:
        :return: no return.
        """
        if await self.get_by_email(email) is not None:
            print(self.get_by_email(email))
            raise UserIsAlreadyExistsError

        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        self.session.add(user)
        await self.session.commit()

    async def add_yandex_oauth_id(self, user_id: int, yandex_id: str) -> None:
        user = await self.get_by_id(user_id)
        user.oauth_yandex_id = yandex_id
        await self.session.merge(user)
        await self.session.commit()