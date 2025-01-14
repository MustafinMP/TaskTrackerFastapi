from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db_models import UserModel, ProjectModel, user_to_project_model
from infrastructure.entities import ProjectDM, MemberDM


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add(self, creator_id: int, project_title: str = None) -> ProjectDM:
        if project_title is None:
            project_title = 'New project'

        project = (await self.session.scalars(
            insert(ProjectModel).returning(ProjectModel),
            [{'creator_id': creator_id, 'title': project_title}]
        )).first()
        project_dm = ProjectDM(
            id=project.id,
            title=project.title,
            creator_id=project.creator_id,
        )
        await self.session.commit()
        return project_dm

    async def add_new_members(self, project_id: int, *new_member_ids: list[int]) -> None:
        """

        :param project_id: the id of the current team.
        :param new_member_ids: the list of ids of new team members.
        :return: no return.
        """

        stmt = select(ProjectModel).where(ProjectModel.id == project_id)
        project = await self.session.scalar(stmt)
        if project is None:
            return
        await self.session.execute(
            insert(user_to_project_model),
            [
                {'user': new_member_id, 'project': project_id}
                for new_member_id in new_member_ids
                if await self.session.scalar(select(UserModel).where(UserModel.id == new_member_id)) is not None
            ]
        )
        await self.session.commit()

    async def get_by_id(self, project_id: int) -> ProjectDM:
        stmt = select(ProjectModel).where(ProjectModel.id == project_id)
        project = await self.session.scalar(stmt)
        return ProjectDM(
            id=project.id,
            title=project.title,
            creator_id=project.creator_id,
        ) if project else None

    async def get_by_member_id(self, member_id: int) -> list[ProjectDM]:
        projects_stmt = select(ProjectModel).join(ProjectModel.members).filter(UserModel.id == member_id)
        projects = (await self.session.scalars(projects_stmt)).unique().fetchall()
        return [
            ProjectDM(
                id=project.id,
                title=project.title,
                creator_id=project.creator_id,
            )
            for project in projects
        ]

    async def get_members(self, project_id: int) -> list[MemberDM]:
        stmt = select(ProjectModel).where(ProjectModel.id == project_id)
        project = await self.session.scalar(stmt)
        return [
            MemberDM(
                id=member.id,
                name=member.name,
                image=member.image
            )
            for member in project.members
        ]
