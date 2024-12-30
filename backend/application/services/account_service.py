from __future__ import annotations
from fastapi import Depends, HTTPException
from starlette import status

import db_session
from application.services.password_hasher import PasswordHasher
from infrastructure.entities.user import UserDM
from infrastructure.repositories.user_repository import UserRepository
from presentation.schemas.user_schemas import AddUserSchema


class UserService:

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserDM | None:
        async with db_session.create_session() as session:
            repository = UserRepository(session)
            return await repository.get_by_id(user_id)

    @staticmethod
    async def get_user_by_email(user_email: str) -> UserDM | None:
        async with db_session.create_session() as session:
            repository = UserRepository(session)
            return await repository.get_by_email(user_email)

    @staticmethod
    async def get_user_by_yandex_uid(uid: int) -> UserDM | None:
        async with db_session.create_session() as session:
            repository = UserRepository(session)
            return await repository.get_by_yandex_id(uid)

    async def add_user(self, user_data: AddUserSchema) -> UserDM:
        if await self.get_user_by_email(user_data.email) is not None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Данный email уже зарегистрирован'
            )
        hashed_password = PasswordHasher().hash_password(user_data.password)
        async with db_session.create_session() as session:
            repository = UserRepository(session)
            await repository.add(
                user_data.name,
                user_data.email,
                hashed_password
            )
            return await repository.get_by_email(user_data.email)
