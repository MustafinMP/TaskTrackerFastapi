from fastapi import Depends

import db_session
from infrastructure.db_models.user_models import UserModel
from application.services.account_service import UserService
from infrastructure.db_models.team_models import TeamModel
from infrastructure.repositories.team_repository import TeamRepository


class TeamService:
    @staticmethod
    async def add_team(creator: UserModel, team_name: str = None) -> None:
        async with db_session.create_session() as session:
            repository = TeamRepository(session)
            await repository.add(creator, team_name)

    @staticmethod
    async def add_new_team_members(team_id: int, *new_member_ids: list[int]) -> None:
        async with db_session.create_session() as session:
            repository = TeamRepository(session)
            await repository.add_new_members(team_id, *new_member_ids)

    @staticmethod
    async def get_user_teams(current_user_id: int) -> list[TeamModel, ...]:
        async with db_session.create_session() as session:
            repository = TeamRepository(session)
            return await repository.get_by_member_id(current_user_id)

    @staticmethod
    async def user_in_team_by_ids(user_id: int, team_id: int) -> bool:
        async with db_session.create_session() as session:
            repository = TeamRepository(session)
            return await repository.have_member_by_ids(user_id, team_id)

    @staticmethod
    async def get_team_by_id(team_id: int) -> TeamModel:
        async with db_session.create_session() as session:
            repository = TeamRepository(session)
            return await repository.get_by_id(team_id)

# def get_team_data_by_id(team_id: int) -> dict:
#     stmt = select(Team).where(
#         Team.id == team_id
#     ).join(Team.members).where(
#         User.id == current_user.id
#     )
#     with db_session.create_session() as session:
#         team = session.scalar(stmt)
#         return team.to_dict(
#             only=(
#                 'name',
#                 'creator.id',
#                 'creator.name',
#                 'members.id',
#                 'members.name'
#             )
#         )
