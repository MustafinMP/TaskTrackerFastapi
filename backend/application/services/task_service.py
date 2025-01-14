from fastapi import Depends

import db_session
from infrastructure.entities import StatusDM
from infrastructure.db_models import UserModel, StatusModel, TaskModel  # !!!
from application.services import UserService, ProjectService
from application.exceptions.task_exceptions import TaskDoesNotExistError, UserPermissionError
from infrastructure.repositories import StatusRepository, TaskRepository


class TaskService:
    @staticmethod
    async def get_tasks_by_status(team_id: int, status: StatusModel) -> list[TaskModel]:
        with db_session.create_session() as session:
            repository = TaskRepository(session)
            return await repository.get_by_status(status.id, team_id)

    @staticmethod
    async def get_task_by_id(task_id: int,
                             current_user_id: int = Depends(UserService.get_current_user_id)) -> TaskModel:
        with db_session.create_session() as session:
            repository = TaskRepository(session)
            task = await repository.get_by_id(task_id)
            if not task:
                raise TaskDoesNotExistError
            if not ProjectService.is_user_project(current_user_id, task.project.id):
                raise UserPermissionError
            return task

    @staticmethod
    async def update_task(
            task_id: int,
            new_name: str = None,
            new_description: str = None,
            new_status_id: int = None,
            current_user_id: int = Depends(UserService.get_current_user_id)
    ) -> None:
        with db_session.create_session() as session:
            repository = TaskRepository(session)
            task = await repository.get_by_id(task_id)
            if not task:
                raise TaskDoesNotExistError
            if not ProjectService.is_user_project(current_user_id, task.project.id):
                raise UserPermissionError
            await repository.update_object(
                task,
                new_name=new_name,
                new_description=new_description,
                new_status_id=new_status_id
            )

    @staticmethod
    def delete_task(task_id: int, current_user: UserModel = Depends(UserService.get_current_user)) -> None:
        with db_session.create_session() as session:
            repository = TaskRepository(session)
            task: TaskModel = repository.get_by_id(task_id)
            if not task:
                raise TaskDoesNotExistError
            if current_user not in task.project.members:
                raise UserPermissionError
            repository.delete_object(task)


class StatusService:
    def __init__(self):
        with db_session.create_session() as session:
            self._repository = StatusRepository(session)

    def get_statuses(self) -> list[StatusDM]:
        return self._repository.get_all()
