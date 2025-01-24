import db_session
from domain.entities import ProjectDM
from infrastructure.repositories import ProjectRepository


class ProjectService:
    @staticmethod
    async def add_project(creator_id: int, project_title: str = None) -> ProjectDM:
        async with db_session.create_session() as session:
            repository = ProjectRepository(session)
            project = await repository.add(creator_id, project_title)
            await repository.add_new_members(project.id, creator_id)
            return project

    @staticmethod
    async def add_new_project_members(project_id: int, *new_member_ids: list[int]) -> None:
        async with db_session.create_session() as session:
            repository = ProjectRepository(session)
            await repository.add_new_members(project_id, *new_member_ids)

    @staticmethod
    async def get_user_projects(current_user_id: int) -> list[ProjectDM, ...]:
        async with db_session.create_session() as session:
            repository = ProjectRepository(session)
            return await repository.get_by_member_id(current_user_id)

    @staticmethod
    async def is_user_project(user_id: int, project_id: int) -> bool:
        async with db_session.create_session() as session:
            repository = ProjectRepository(session)
            members = await repository.get_members(project_id)
            return any([user_id == member.id for member in members])

    @staticmethod
    async def get_project_by_id(project_id: int) -> ProjectDM:
        async with db_session.create_session() as session:
            repository = ProjectRepository(session)
            return await repository.get_by_id(project_id)
