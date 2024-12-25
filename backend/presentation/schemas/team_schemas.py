from pydantic import BaseModel

from presentation.schemas.user_schemas import UserSchema


class TeamSchema(BaseModel):
    id: int
    name: str
    creator_id: int
    members = list[UserSchema]
    creator = UserSchema
