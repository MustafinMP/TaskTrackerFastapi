from dataclasses import asdict

from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db_models import TaskModel, TagModel, ProjectModel
from infrastructure.entities import CreateTaskDM, TaskToTagRelationDM, UpdateTaskDM, TaskDM


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def create(self, task_data: CreateTaskDM) -> None:
        """Create new task and save it to database.

        :param task_data:
        :return: no return.
        """

        task = (await self.session.scalars(
            insert(TaskModel).returning(TaskModel),
            [asdict(task_data)]
        )).first()
        task_dm = TaskDM(
            id=task.id,
            title=task.name,
            description=task.description,
            project_id=task.project_id,
            creator_id=task.creator_id,
            created_date=task.created_date,
            deadline=task.deadline,
            status_id=task.status_id
        )
        await self.session.commit()
        return task_dm

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

    async def get_by_id(self, task_id: int) -> TaskDM | None:
        """Find task by id.

        :param task_id:
        :param task_id: the id of task.
        :return: task object or none.
        """

        stmt = select(TaskModel).where(
            TaskModel.id == task_id
        )
        task: TaskModel = await self.session.scalar(stmt)
        return TaskDM(
            id=task.id,
            title=task.name,
            description=task.description,
            project_id=task.project_id,
            creator_id=task.creator_id,
            created_date=task.created_date,
            deadline=task.deadline,
            status_id=task.status_id
        ) if task else None

    async def get_by_status(self, status_id: int) -> list[TaskDM]:
        """Find tasks by their status.

        :param status_id: the id of task status.
        :return: list of tasks with current status.
        """

        stmt = select(TaskModel).where(
            TaskModel.status_id == status_id
        )
        tasks: list[TaskModel] = (await self.session.scalars(stmt)).unique().all()
        return [
            TaskDM(
                id=task.id,
                title=task.name,
                description=task.description,
                project_id=task.project_id,
                creator_id=task.creator_id,
                created_date=task.created_date,
                deadline=task.deadline,
                status_id=task.status_id
            )
            for task in tasks
        ]

    async def get_by_project_id(self, project_id: int) -> list[TaskDM]:
        stmt = select(TaskModel).join(TaskModel.project).filter(
            ProjectModel.id == project_id
        )
        tasks: list[TaskModel] = (await self.session.scalars(stmt)).unique().all()
        return [
            TaskDM(
                id=task.id,
                title=task.name,
                description=task.description,
                project_id=task.project_id,
                creator_id=task.creator_id,
                created_date=task.created_date,
                deadline=task.deadline,
                status_id=task.status_id
            )
            for task in tasks
        ]

    async def update(
            self,
            new_task_data: UpdateTaskDM
    ) -> TaskDM | None:
        """Update information about current task.

        :param new_task_data:
        :return: no return.
        """

        values = asdict(new_task_data)
        del values['id']
        for key, value in values.items():
            if value is None:
                del values[key]

        stmt = update(TaskModel).where(
            TaskModel.id == new_task_data.id,
        ).values(**values)
        await self.session.execute(stmt)
        await self.session.commit()
        return self.get_by_id(new_task_data.id)  # доделать проверку на существование задачи и статуса

    async def delete_by_id(self, task_id: int) -> None:
        """Delete the task from database by id.

        :param task_id: the id of the task.
        :return: no return.
        """

        stmt = delete(TaskModel).where(
            TaskModel.id == task_id
        )
        await self.session.execute(stmt)
        await self.session.commit()
