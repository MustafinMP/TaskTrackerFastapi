from fastapi import APIRouter, Depends

from application.services.project_service import ProjectService
from presentation.cookie_manager import CookieManager

router = APIRouter(
    prefix='/projects',
    tags=['projects']
)


@router.get('/all')
async def user_projects(user_id: int = Depends(CookieManager().get_current_user_id)):
    return [
        project.to_dict(only=['id', 'title', 'members.image'])
        for project in ProjectService.get_user_projects(user_id)
    ]


@router.get('/{project_id}')
async def get_project(project_id: int):
    project = await ProjectService.get_project_by_id(project_id)
    return project.to_dict(only=['id', 'title', 'members.image'])


@router.get('/create-project')
async def create_team(user_id: int = Depends(CookieManager().get_current_user_id)):
    await ProjectService.add_project(user_id, 'Test project')
    return {'status': 'ok'}
