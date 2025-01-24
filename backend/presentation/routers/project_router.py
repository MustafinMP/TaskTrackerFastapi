from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from application.services.project_service import ProjectService
from presentation.cookie_manager import CookieManager

router = APIRouter(
    prefix='/projects',
    tags=['projects']
)

cookie = CookieManager()


@router.get('/all')
async def user_projects(user_id: int | None = Depends(cookie.get_current_user_id)):
    # if user_id is not None:
    try:
        projects = await ProjectService.get_user_projects(user_id)
        return projects
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get('/{project_id}')
async def get_project(project_id: int):
    project = await ProjectService.get_project_by_id(project_id)
    return project


@router.get('/create-project')
async def create_team(user_id: int = Depends(cookie.get_current_user_id)):
    new_project = await ProjectService.add_project(user_id, 'Test project')
    return new_project
