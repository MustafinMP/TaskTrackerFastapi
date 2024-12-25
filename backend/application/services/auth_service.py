import requests
from fastapi import HTTPException, Depends
from starlette import status

import db_session
from infrastructure.db_models.user_models import UserModel
from infrastructure.repositories.user_repository import UserRepository
from presentation.schemas.user_schemas import LoginFormSchema, RegisterFormSchema
from application.services.account_service import UserService
from config import YA_CLIENT_ID, YA_CLIENT_SECRET
from application.services.team_service import TeamService


class AuthService:
    @staticmethod
    async def login_user_for_id(form: LoginFormSchema) -> int:
        user: UserModel = await UserService.get_user_by_email(form.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Пользователь не зарегистрирован'
            )
        if not user.check_password(form.password):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Неверный пароль'
            )
        return user.id

    @staticmethod
    async def register_user(form: RegisterFormSchema) -> None:
        if form.password != form.password_again:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Пароли не совпадают'
            )
        user = await UserService.add_user(form)
        await TeamService.add_team(user)

    # @staticmethod
    # def yandex_callback(code) -> None:
    #     token_url = 'https://oauth.yandex.ru/token'
    #     token_params = {
    #         'grant_type': 'authorization_code',
    #         'code': code,
    #         'client_id': YA_CLIENT_ID,
    #         'client_secret': YA_CLIENT_SECRET
    #     }
    #     response = requests.post(token_url, data=token_params)
    #     data = response.json()
    #     if 'access_token' in data:
    #         user_info_url = 'https://login.yandex.ru/info'
    #         headers = {'Authorization': f'OAuth {data['access_token']}'}
    #         user_info_response = requests.post(user_info_url, headers=headers)
    #         user_info = user_info_response.json()
    #         yandex_uid = str(user_info.get('id'))
    #         AuthService.login_by_yandex_uid(yandex_uid)
    #
    # @staticmethod
    # def login_by_yandex_uid(uid: str, current_user: UserModel = Depends(UserService.get_current_user)) -> None:
    #     with db_session.create_session() as session:
    #         repository = UserRepository(session)
    #         user = repository.get_by_yandex_id(uid)
    #         # if current_user is None:
    #         #     login_user(user, remember=True)
    #         #     return
    #         # if current_user.oauth_yandex_id is None:
    #         #     repository.add_yandex_oauth_id(current_user.id, uid)