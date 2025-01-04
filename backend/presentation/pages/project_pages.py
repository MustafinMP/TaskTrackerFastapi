from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/projects',
    tags=['projects']
)

templates = Jinja2Templates(directory='../frontend/templates')


@router.get('/projects')
def projects(request: Request):
    return templates.TemplateResponse('projects/projects.html', {'request': request})
