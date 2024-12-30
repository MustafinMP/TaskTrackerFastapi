from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db_models.user_models import UserModel
from infrastructure.entities.team import TeamDM, MemberDM
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.db_models.team_models import TeamModel, user_to_team


class TeamRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add(self, creator_id: int, team_name: str = None) -> None:
        new_team = TeamModel()
        new_team.creator_id = creator_id
        if team_name is None:
            team_name = 'New team'
        new_team.name = team_name
        self.session.add(new_team)
        await self.session.commit()

    async def add_new_members(self, team_id: int, *new_member_ids: list[int]) -> None:
        """

        :param team_id: the id of the current team.
        :param new_member_ids: the list of ids of new team members.
        :return: no return.
        """

        team = await self.get_by_id(team_id)
        user_repository = UserRepository(self.session)
        for new_member_id in new_member_ids:
            member = await user_repository.get_by_id(new_member_id)
            if member is not None:
                team.members.append(member)
                self.session.add(team)
        await self.session.commit()

    async def get_by_id(self, team_id: int) -> TeamDM:
        stmt = select(TeamModel).where(TeamModel.id == team_id)
        team = await self.session.scalar(stmt)
        return TeamDM(
            id=team.id,
            name=team.name,
            creator_id=team.creator_id,
            members=[
                MemberDM(id=member.id, name=member.name, image=member.image)
                for member in team.members
            ]
        )

    async def get_by_member_id(self, member_id: int) -> list[TeamDM]:
        teams_stmt = select(TeamModel).join(TeamModel.members).filter(UserModel.id == member_id)
        teams = (await self.session.scalars(teams_stmt)).unique().fetchall()
        return [
            TeamDM(
                id=team.id,
                name=team.name,
                creator_id=team.creator_id,
                members=[
                    MemberDM(id=member.id, name=member.name, image=member.image)
                    for member in team.members
                ]
            )
            for team in teams
        ]
