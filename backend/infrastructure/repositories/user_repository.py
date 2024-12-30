from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db_session import create_session
from infrastructure.entities.user import UserDM
from infrastructure.exceptions.user_exceptions import UserIsAlreadyExistsError
from infrastructure.db_models.user_models import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_by_id(self, user_id: int) -> UserDM | None:
        """Find user in database by id.

        :param user_id: the id of the user.
        :return: user object or none.
        """

        stmt = select(UserModel).where(UserModel.id == user_id)  # .options(joinedload(UserModel.projects))
        user = await self.session.scalar(stmt)
        return UserDM(
            id=user.id,
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            created_at=user.created_date,
            image=user.image,
            yandex_id=user.oauth_yandex_id
        )

    async def get_by_email(self, user_email: str) -> UserDM | None:
        """Find user in database by email.

        :param user_email: the email of the user.
        :return: user object or none.
        """

        stmt = select(UserModel).where(UserModel.email == user_email)
        user = await self.session.scalar(stmt)

        return UserDM(
            id=user.id,
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            created_at=user.created_date,
            image=user.image,
            yandex_id=user.oauth_yandex_id
        ) if user else None

    async def get_by_yandex_id(self, yandex_id: int) -> UserDM | None:
        """Find user in database by id.

        :param yandex_id: the yandex oauth id of the user.
        :return: user object or none.
        """

        stmt = select(UserModel).where(UserModel.oauth_yandex_id == yandex_id)  # .options(joinedload(UserModel.projects))
        user = await self.session.scalar(stmt)
        return UserDM(
            id=user.id,
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            created_at=user.created_date,
            image=user.image,
            yandex_id=user.oauth_yandex_id
        )

    async def add(self, name: str, email: str, hashed_password: str) -> int:
        """Create new user by data from register form.

        :param name:
        :param email:
        :param hashed_password:
        :return: no return.
        """
        if await self.get_by_email(email) is not None:
            print(self.get_by_email(email))
            raise UserIsAlreadyExistsError

        user = UserModel()
        user.name = name
        user.email = email
        user.hashed_password = hashed_password
        self.session.add(user)
        await self.session.commit()

    async def add_yandex_oauth_id(self, user_id: int, yandex_id: str) -> None:
        user = await self.get_by_id(user_id)
        user.oauth_yandex_id = yandex_id
        await self.session.merge(user)
        await self.session.commit()
