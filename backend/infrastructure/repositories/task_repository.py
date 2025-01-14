from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from infrastructure.db_models import TaskModel, TagModel, ProjectModel
from infrastructure.entities import CreateTaskDM, TaskToTagRelationDM, UpdateTaskDM


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add(
            self,
            task: CreateTaskDM
    ) -> None:
        """Create new task and save it to database.

        :param task:
        :return: no return.
        """

        task_model = TaskModel()
        task_model.name = task.name
        task_model.description = task.description
        task_model.project_id = task.team_id
        if task.deadline is not None:
            task_model.deadline = task.deadline
        if task.status_id is not None:
            task_model.status_id = task.status_id
        task_model.creator_id = task.creator_id
        self.session.add(task_model)
        await self.session.commit()

    async def add_tag_to_task(self, relation: TaskToTagRelationDM) -> None:
        """Add tag to task.

        :param relation:
        :return: no return.
        """

        task_stmt = select(TaskModel).where(
            TaskModel.id == relation.task_id
        )
        tag_stmt = select(TagModel).where(
            TagModel.id == relation.tag_id
        )
        task: TaskModel = self.session.scalar(task_stmt)
        tag: TagModel = self.session.scalar(tag_stmt)
        tag.tasks.append(task)
        await self.session.commit()

    async def get_by_id(self, task_id: int) -> TaskModel | None:
        """Find task by id.

        :param task_id:
        :param task_id: the id of task.
        :return: task object or none.
        """

        stmt = select(TaskModel).where(
            TaskModel.id == task_id
        )
        # .join(Task.team).filter(
        #     Team.id == team_id
        # ).options(
        #     joinedload(Task.creator)
        # ))
        return await self.session.scalar(stmt)  # !!!

    async def get_by_status(self, status_id: int, team_id: int) -> list[TaskModel, ...]:
        """Find tasks by their status.

        :param team_id: the id of team.
        :param status_id: the id of task status.
        :return: list of tasks with current status.
        """

        stmt = select(TaskModel).where(
            TaskModel.status_id == status_id
        ).join(TaskModel.project).filter(
            ProjectModel.id == team_id
        )
        return (await self.session.scalars(stmt)).unique().all()  # !!!

    async def get_by_team_id(self, team_id: int) -> list[TaskModel, ...]:
        stmt = select(TaskModel).join(TaskModel.project).filter(
            ProjectModel.id == team_id
        ).options(
            joinedload(TaskModel.creator)
        )

        return (await self.session.scalars(stmt)).unique()  # !!!

    async def count_by_team_id(self, team_id: int) -> int:
        stmt = select(func.count()).select_from(TaskModel).join(TaskModel.project).filter(
            ProjectModel.id == team_id
        )
        return await self.session.scalar(stmt)

    async def update_by_id(
            self,
            new_task_data: UpdateTaskDM
    ) -> None:
        """Update information about current task.

        :param new_task_data:
        :return: no return.
        """

        values = dict()
        if new_task_data.name:
            values['name'] = new_task_data.name
        if new_task_data.description:
            values['description'] = new_task_data.description
        if new_task_data.status_id:
            values['status_id'] = new_task_data.status_id

        stmt = update(TaskModel).where(
            TaskModel.id == new_task_data.id,
        ).values(**values)
        await self.session.execute(stmt)
        await self.session.commit()  # !!!

    async def update_object(
            self,
            task: TaskModel,
            new_name: str = None,
            new_description: str = None,
            new_status_id: int = None
    ) -> None:
        if new_name:
            task.name = new_name
        if new_description:
            task.description = new_description
        if new_status_id is not None:
            task.status_id = new_status_id
        await self.session.merge(task)
        await self.session.commit()  # !!!

    async def delete_by_id(self, task_id: int) -> None:
        """Delete the task from database by id.

        :param task_id: the id of the task.
        :return: no return.
        """

        stmt = delete(TaskModel).where(
            TaskModel.id == task_id
        )
        await self.session.execute(stmt)
        await self.session.commit()  # !!!

    async def delete_object(self, task: TaskModel) -> None:
        await self.session.delete(task)
        await self.session.commit()  # !!!
