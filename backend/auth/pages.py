from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/auth',
    tags=['pages']
)

templates = Jinja2Templates(directory='../frontend/templates')


@router.get('/login')
def login(request: Request):
    return templates.TemplateResponse('auth/login.html', {'request': request})


@router.get('/register')
def register(request: Request):
    return templates.TemplateResponse('auth/register.html', {'request': request})