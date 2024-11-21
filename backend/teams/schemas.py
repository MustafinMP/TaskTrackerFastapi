from pydantic import BaseModel

from auth.schemas import UserSchema


class TeamSchema(BaseModel):
    id: int
    name: str
    creator_id: int
    members = list[UserSchema]
    creator = UserSchema
