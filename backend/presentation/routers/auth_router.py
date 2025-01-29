from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import Response

from application.exceptions import EmailIsAlreadyExists, WrongPassword, EmailDoesntExist
from application.services import AuthService
from presentation.cookie_manager import CookieManager
from presentation.schemas import RegisterFormSchema, LoginFormSchema
from config import YANDEX_API_REQUEST

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


@router.post('/register')
async def register(
        form: RegisterFormSchema
):
    try:
        await AuthService().register_user(form)
        return
    except EmailIsAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Данный email уже зарегистрирован'
        )
    except WrongPassword:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Пароли не совпадают'
        )


@router.post('/login')
async def login(
        form: LoginFormSchema,
        response: Response,
        cookie_manager: CookieManager = Depends(CookieManager)
):
    try:
        user_id = await AuthService().login_user_for_id(form)
        cookie_manager.set_cookie(response, user_id)
        return user_id
    except WrongPassword:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Неверный логин или пароль'
        )
    except EmailDoesntExist:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Неверный логин или пароль'
        )


# @router.get('/yandex-login')
# async def yandex_login():
#     """Register or sign in by means of Yandex Account."""
#     redirect_url = YANDEX_API_REQUEST
#     return RedirectResponse(redirect_url)

#
# @router.get('/yandex-callback')
# async def yandex_callback(request: Request, response: Response):
#     """Fetch a response from Yandex."""
#     code = request.query_params['code']
#     if code:
#         oauth2yandex.callback(code)
#     return RedirectResponse('/')
