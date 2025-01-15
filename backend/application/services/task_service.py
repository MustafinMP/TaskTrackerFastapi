import db_session
from infrastructure.entities import TaskDM, UpdateTaskDM
from application.services import ProjectService
from application.exceptions.task_exceptions import TaskDoesNotExistError, UserPermissionError
from infrastructure.repositories import TaskRepository


class TaskService:
    @staticmethod
    async def get_tasks_by_status(status_id: int, user_id: int) -> list[TaskDM]:
        with db_session.create_session() as session:
            repository = TaskRepository(session)
            tasks = [
                task
                for task in await repository.get_by_status(status_id)
                if ProjectService.is_user_project(user_id, task.project_id)
            ]
            return tasks

    @staticmethod
    async def get_task_by_id(task_id: int,
                             user_id: int) -> TaskDM:
        with db_session.create_session() as session:
            task_repository = TaskRepository(session)
            task = await task_repository.get_by_id(task_id)
        if not task:
            raise TaskDoesNotExistError
        if not ProjectService.is_user_project(user_id, task.project_id):
            raise UserPermissionError
        return task

    @staticmethod
    async def update_task(
            task_id: int,
            user_id: int,
            new_title: str = None,
            new_description: str = None,
            new_status_id: int = None,
            new_deadline: int = None
    ) -> None:
        with db_session.create_session() as session:
            repository = TaskRepository(session)
            task = await repository.get_by_id(task_id)
            if not task:
                raise TaskDoesNotExistError
            if not ProjectService.is_user_project(user_id, task.project_id):
                raise UserPermissionError
            return await repository.update(
                UpdateTaskDM(
                    id=task_id,
                    title=new_title,
                    description=new_description,
                    status_id=new_status_id,
                    deadline=new_deadline
                )
            )

    @staticmethod
    async def delete_task(task_id: int, user_id: int) -> None:
        with db_session.create_session() as session:
            repository = TaskRepository(session)
            task = await repository.get_by_id(task_id)
            if not task:
                raise TaskDoesNotExistError
            if not ProjectService.is_user_project(user_id, task.project_id):
                raise UserPermissionError
            await repository.delete_by_id(task_id)
