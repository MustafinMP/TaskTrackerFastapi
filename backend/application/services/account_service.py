from fastapi import Depends, HTTPException
from starlette import status

import db_session
from infrastructure.db_models.user_models import UserModel
from infrastructure.repositories.user_repository import UserRepository
from presentation.schemas.user_schemas import AddUserSchema


class UserService:

    # @staticmethod
    # async def get_user_by_id(user_id: int) -> UserModel:
    #     return await UserService.get_user_by_id(user_id)

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserModel | None:
        async with db_session.create_session() as session:
            repository = UserRepository(session)
            return await repository.get_by_id(user_id)

    @staticmethod
    async def get_user_by_email(user_email: str) -> UserModel | None:
        async with db_session.create_session() as session:
            repository = UserRepository(session)
            return await repository.get_by_email(user_email)

    @staticmethod
    async def get_user_by_yandex_uid(uid: int) -> UserModel | None:
        async with db_session.create_session() as session:
            repository = UserRepository(session)
            return await repository.get_by_yandex_id(uid)

    @staticmethod
    async def add_user(user_data: AddUserSchema) -> int:
        if await UserService.get_user_by_email(user_data.email) is not None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Данный email уже зарегистрирован'
            )
        async with db_session.create_session() as session:
            user_repository = UserRepository(session)
            await user_repository.add(
                user_data.name,
                user_data.email,
                user_data.password
            )
            return await user_repository.get_by_email(user_data.email)
