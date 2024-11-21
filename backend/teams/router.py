from fastapi import APIRouter

from teams.service import TeamService

router = APIRouter(
    prefix='/teams',
    tags=['teams']
)


@router.get('/all')
def user_teams():
    return [
        team.to_dict(only=['id', 'name', 'members.image'])
        for team in TeamService.get_user_teams()
    ]


@router.get('/{team_id}')
async def single_team(team_id: int):
    team = await TeamService.get_team_by_id(team_id)
    return team.to_dict(only=['id', 'name', 'members.image'])