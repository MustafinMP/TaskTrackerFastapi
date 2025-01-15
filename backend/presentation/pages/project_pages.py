from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/projects',
    tags=['pages']
)

templates = Jinja2Templates(directory='../frontend/templates')


@router.get('/')
def projects(request: Request):
    return templates.TemplateResponse('projects/projects.html', {'request': request})


@router.get('/{project_id}')
def project(request: Request, project_id: int):
    return templates.TemplateResponse('projects/project.html', {'request': request})
