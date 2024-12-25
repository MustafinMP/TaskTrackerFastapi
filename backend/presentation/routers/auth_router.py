from typing import Annotated

from fastapi import APIRouter,  Form
from starlette.responses import Response, RedirectResponse

from application.services.auth_service import AuthService
from presentation.schemas.user_schemas import RegisterFormSchema, LoginFormSchema
from config import YANDEX_API_REQUEST

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


@router.post('/register')
async def register(form: Annotated[RegisterFormSchema, Form()]):
    await AuthService.register_user(form)
    return RedirectResponse('/auth/login')


@router.post('/login')
async def login_cookie(response: Response, form: Annotated[LoginFormSchema, Form()]):
    await AuthService.login_user(response, form)
    return {'result': 'ok'}


@router.get('/yandex-login')
async def yandex_login():
    """Register or sign in by means of Yandex Account."""
    redirect_url = YANDEX_API_REQUEST
    return RedirectResponse(redirect_url)

#
# @router.get('/yandex-callback')
# async def yandex_callback(request: Request, response: Response):
#     """Fetch a response from Yandex."""
#     code = request.query_params['code']
#     if code:
#         oauth2yandex.callback(code)
#     return RedirectResponse('/')