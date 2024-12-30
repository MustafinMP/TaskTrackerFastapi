from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db_models.user_models import UserModel
from infrastructure.entities.project import ProjectDM, MemberDM
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.db_models.project_models import ProjectModel


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add(self, creator_id: int, project_title: str = None) -> None:
        new_project = ProjectModel()
        new_project.creator_id = creator_id
        if project_title is None:
            project_title = 'New project'
        new_project.title = project_title
        self.session.add(new_project)
        await self.session.commit()

    async def add_new_members(self, project_id: int, *new_member_ids: list[int]) -> None:
        """

        :param project_id: the id of the current team.
        :param new_member_ids: the list of ids of new team members.
        :return: no return.
        """

        project = await self.get_by_id(project_id)
        user_repository = UserRepository(self.session)
        for new_member_id in new_member_ids:
            member = await user_repository.get_by_id(new_member_id)
            if member is not None:
                project.members.append(member)
                self.session.add(project)
        await self.session.commit()

    async def get_by_id(self, project_id: int) -> ProjectDM:
        stmt = select(ProjectModel).where(ProjectModel.id == project_id)
        project = await self.session.scalar(stmt)
        return ProjectDM(
            id=project.id,
            title=project.title,
            creator_id=project.creator_id,
            members=[
                MemberDM(id=member.id, name=member.name, image=member.image)
                for member in project.members
            ]
        )

    async def get_by_member_id(self, member_id: int) -> list[ProjectDM]:
        projects_stmt = select(ProjectModel).join(ProjectModel.members).filter(UserModel.id == member_id)
        projects = (await self.session.scalars(projects_stmt)).unique().fetchall()
        return [
            ProjectDM(
                id=project.id,
                title=project.title,
                creator_id=project.creator_id,
                members=[
                    MemberDM(id=member.id, name=member.name, image=member.image)
                    for member in project.members
                ]
            )
            for project in projects
        ]
