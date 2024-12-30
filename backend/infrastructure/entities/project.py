from dataclasses import dataclass
from typing import Optional


@dataclass
class MemberDM:
    id: int
    name: str
    image: Optional[str]


@dataclass
class ProjectDM:
    id: int
    title: str
    creator_id: int
    members: list[MemberDM]
