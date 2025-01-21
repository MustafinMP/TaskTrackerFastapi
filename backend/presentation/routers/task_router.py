from fastapi import APIRouter, Depends
from starlette import status
from starlette.exceptions import HTTPException

from application.exceptions.task_exceptions import UserPermissionError
from application.services import TaskService
from infrastructure.entities import CreateTaskDM
from presentation.cookie_manager import CookieManager
from presentation.schemas.task_schemas import CreateTaskSchema

router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)


@router.get('/')
async def tasks_by_project(project: int, user_id: int = Depends(CookieManager().get_current_user_id)):
    tasks = await TaskService.get_tasks_by_project_id(project, user_id)
    return tasks


@router.post('/create')
async def create_task(task: CreateTaskSchema, user_id: int = Depends(CookieManager().get_current_user_id)):
    task_dm = CreateTaskDM(
        title=task.title,
        description=task.description,
        creator_id=user_id,
        project_id=task.project_id,
        deadline=task.deadline,
        status_id=task.status_id
    )
    try:
        created_task = await TaskService.create_task(task_dm)
        return created_task
    except UserPermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Нет прав доступа'
        )