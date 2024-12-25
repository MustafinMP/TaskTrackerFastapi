from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db_models.user_models import UserModel
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.db_models.team_models import TeamModel, user_to_team


class TeamRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add(self, creator: UserModel, team_name: str = None) -> None:
        new_team = TeamModel()
        new_team.creator_id = creator.id
        if team_name is None:
            team_name = 'New team'
        new_team.name = team_name
        new_team.members.append(creator)
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

    async def get_by_id(self, team_id: int) -> TeamModel:
        stmt = select(TeamModel).where(TeamModel.id == team_id)
        return await self.session.scalar(stmt)

    async def get_by_member_id(self, member_id: int) -> list[TeamModel]:
        teams_stmt = select(TeamModel).join(TeamModel.members).filter(UserModel.id == member_id)
        return (await self.session.scalars(teams_stmt)).unique().fetchall()

    async def have_member_by_ids(self, user_id: int, team_id: int) -> bool:
        stmt = select(user_to_team).where(
            and_(
                user_to_team.c.user == user_id,
                user_to_team.c.team == team_id,
            )
        )
        return await self.session.scalar(stmt) is not None
