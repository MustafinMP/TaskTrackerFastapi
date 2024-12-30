import db_session
from infrastructure.db_models.project_models import ProjectModel
from infrastructure.repositories.project_repository import ProjectRepository


class ProjectService:
    @staticmethod
    async def add_project(creator_id: int, project_title: str = None) -> None:
        async with db_session.create_session() as session:
            repository = ProjectRepository(session)
            await repository.add(creator_id, project_title)

    @staticmethod
    async def add_new_project_members(project_id: int, *new_member_ids: list[int]) -> None:
        async with db_session.create_session() as session:
            repository = ProjectRepository(session)
            await repository.add_new_members(project_id, *new_member_ids)

    @staticmethod
    async def get_user_projects(current_user_id: int) -> list[ProjectModel, ...]:
        async with db_session.create_session() as session:
            repository = ProjectRepository(session)
            return await repository.get_by_member_id(current_user_id)

    @staticmethod
    async def is_user_project(user_id: int, project_id: int) -> bool:  # переписать
        async with db_session.create_session() as session:
            repository = ProjectRepository(session)
            project = await repository.get_by_id(project_id)
            return any([user_id == member.id for member in project.members])

    @staticmethod
    async def get_project_by_id(project_id: int) -> ProjectModel:
        async with db_session.create_session() as session:
            repository = ProjectRepository(session)
            return await repository.get_by_id(project_id)
