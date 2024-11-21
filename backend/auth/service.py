import uuid
from time import time
from typing import Any

from fastapi import Depends, Cookie, HTTPException
from starlette import status
from starlette.responses import Response

import db_session
from auth.models import User
from auth.repository import UserRepository
from auth.schemas import AddUserSchema

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = 'session-id'


class CookieService:
    @staticmethod
    async def set_cookie(response: Response, email: str = None, yandex_uid: str = None) -> None:
        session_id = uuid.uuid4().hex  # generate_code
        response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
        if email is not None:
            user_id = (await UserService.get_user_by_email(email)).id
        elif yandex_uid is not None:
            user_id = (await UserService.get_user_by_yandex_uid(yandex_uid)).id
        else:
            raise Exception
        COOKIES[session_id] = {'user_id': user_id, 'login_at': int(time())}

    @staticmethod
    def get_session_data(session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)) -> dict[str, Any]:
        if session_id not in COOKIES:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return COOKIES[session_id]


class UserService:
    @staticmethod
    async def get_current_user_id(user_session_data: dict = Depends(CookieService.get_session_data)) -> User:
        user_id = user_session_data.get('user_id', None)
        return user_id

    @staticmethod
    async def get_current_user(user_session_data: dict = Depends(CookieService.get_session_data)) -> User:
        user_id = user_session_data.get('user_id', None)
        return await UserService.get_user_by_id(user_id)

    @staticmethod
    async def get_user_by_id(user_id: int) -> User | None:
        async with db_session.create_session() as session:
            repository = UserRepository(session)
            return await repository.get_by_id(user_id)

    @staticmethod
    async def get_user_by_email(user_email: str) -> User | None:
        async with db_session.create_session() as session:
            repository = UserRepository(session)
            return await repository.get_by_email(user_email)

    @staticmethod
    async def get_user_by_yandex_uid(uid: int) -> User | None:
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
