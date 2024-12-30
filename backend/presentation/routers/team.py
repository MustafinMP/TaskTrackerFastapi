from fastapi import APIRouter, Depends

from application.services.team_service import TeamService
from presentation.cookie_manager import CookieManager

router = APIRouter(
    prefix='/teams',
    tags=['teams']
)


@router.get('/all')
async def user_teams(user_id: int = Depends(CookieManager().get_current_user_id)):
    return [] # [
    #     team.to_dict(only=['id', 'name', 'members.image'])
    #     for team in TeamService.get_user_teams(user_id)
    # ]


# @router.get('/{team_id}')
# async def single_team(team_id: int):
#     team = await TeamService.get_team_by_id(team_id)
#     return team.to_dict(only=['id', 'name', 'members.image'])


@router.get('/create_team')
async def create_team(user_id: int = Depends(CookieManager().get_current_user_id)):
    await TeamService.add_team(user_id, 'Test team')
    return {'status': 'ok'}
