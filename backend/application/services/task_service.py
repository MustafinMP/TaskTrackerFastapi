from fastapi import Depends

import db_session
from infrastructure.db_models.user_models import User
from application.services.account_service import UserService
from exceptions.task_exceptions import TaskDoesNotExistError, UserPermissionError
from infrastructure.db_models.task_models import Status, Task
from infrastructure.repositories.task_repository import TaskRepository, StatusRepository
from application.services.team_service import TeamService


# def add_task(name: str, description: str, deadline: datetime | None = None, status_id: int | None = None) -> None:
#     with db_session.create_session() as session:
#         repository = TaskRepository(session)
#         repository.add(
#             current_user.id,
#             current_user.current_team_id,
#             name,
#             description,
#             deadline,
#             status_id
#         )


class TaskService:
    @staticmethod
    async def get_tasks_by_status(team_id: int, status: Status) -> list[Task]:
        with db_session.create_session() as session:
            repository = TaskRepository(session)
            return await repository.get_by_status(status.id, team_id)

    @staticmethod
    async def get_task_by_id(task_id: int, current_user_id: int = Depends(UserService.get_current_user_id)) -> Task:
        with db_session.create_session() as session:
            repository = TaskRepository(session)
            task = await repository.get_by_id(task_id)
            if not task:
                raise TaskDoesNotExistError
            if not TeamService.user_in_team_by_ids(current_user_id, task.team.id):
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
            if not TeamService.user_in_team_by_ids(current_user_id, task.team.id):
                raise UserPermissionError
            await repository.update_object(
                task,
                new_name=new_name,
                new_description=new_description,
                new_status_id=new_status_id
            )

    @staticmethod
    def delete_task(task_id: int, current_user: User = Depends(UserService.get_current_user)) -> None:
        with db_session.create_session() as session:
            repository = TaskRepository(session)
            task: Task = repository.get_by_id(task_id)
            if not task:
                raise TaskDoesNotExistError
            if current_user not in task.team.members:
                raise UserPermissionError
            repository.delete_object(task)

    @staticmethod
    def get_statuses() -> list[Status]:
        with db_session.create_session() as session:
            repository = StatusRepository(session)
            return repository.get_all()
