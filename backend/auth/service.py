import uuid
from time import time
from typing import Any

import requests
from fastapi import Depends, Cookie, HTTPException
from starlette import status
from starlette.responses import Response

import db_session
from auth.models import User
from auth.repository import UserRepository
from auth.schemas import RegisterFormSchema, LoginFormSchema
from config import YA_CLIENT_ID, YA_CLIENT_SECRET

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = 'session-id'


class CookieService:
    @staticmethod
    def set_cookie(response: Response, form: LoginFormSchema) -> None:
        session_id = uuid.uuid4().hex  # generate_code
        response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
        COOKIES[session_id] = {'username': form.name, 'login_at': int(time())}

    @staticmethod
    def get_session_data(session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)) -> dict[str, Any]:
        if session_id not in COOKIES:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return COOKIES[session_id]


class UserService:
    @staticmethod
    async def get_current_user(user_session_data: dict = Depends(CookieService.get_session_data)):
        username = user_session_data.get('username', None)
        return {'username': username}

    @staticmethod
    async def get_user_by_email(user_email: str) -> User | None:
        """Find user in database by email.

        :param user_email: the email of the user.
        :return: user object or none.
        """

        async with db_session.create_session() as session:
            repository = UserRepository(session)
            user = await repository.get_by_email(user_email)
            return user

    @staticmethod
    async def user_exists_by_email(user_email: str) -> bool:
        """Check that user exists in database.

        :param user_email: the email of the user.
        :return: user object or none.
        """

        return await UserService.get_user_by_email(user_email) is not None


class AuthService:
    @staticmethod
    def login_user(response: Response, form: LoginFormSchema) -> None:
        CookieService.set_cookie(response, form)

    @staticmethod
    async def register_user(form: RegisterFormSchema) -> None:
        if form.password != form.password_again:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Пароли не совпадают'
            )
        if await UserService.user_exists_by_email(form.email):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Данный email уже зарегистрирован'
            )
        async with db_session.create_session() as session:
            user_repository = UserRepository(session)
            await user_repository.add(
                form.name,
                form.email,
                form.password
            )
        # user = user_repository.get_by_email(form.email)
        # team_repository = TeamRepository(session)
        # team_repository.add(user.id, team_name=f"Personal {user.name}'s team")

    @staticmethod
    def callback(code) -> None:
        token_url = 'https://oauth.yandex.ru/token'
        token_params = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': YA_CLIENT_ID,
            'client_secret': YA_CLIENT_SECRET
        }
        response = requests.post(token_url, data=token_params)
        data = response.json()
        if 'access_token' in data:
            user_info_url = 'https://login.yandex.ru/info'
            headers = {'Authorization': f'OAuth {data['access_token']}'}
            user_info_response = requests.post(user_info_url, headers=headers)
            user_info = user_info_response.json()
            yandex_uid = str(user_info.get('id'))
            AuthService.login_by_yandex_uid(yandex_uid)

    @staticmethod
    def login_by_yandex_uid(uid: str, current_user: dict = Depends(UserService.get_current_user)) -> None:
        with db_session.create_session() as session:
            repository = UserRepository(session)
            user = repository.get_by_yandex_id(uid)
            # if current_user is None:
            #     login_user(user, remember=True)
            #     return
            # if current_user.oauth_yandex_id is None:
            #     repository.add_yandex_oauth_id(current_user.id, uid)

