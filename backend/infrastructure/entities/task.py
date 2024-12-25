# from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from infrastructure.entities.status import StatusDTO


@dataclass
class TaskDTO:
    id: int
    name: str
    description: str
    creator_id: Optional[int]
    created_date: datetime
    deadline: Optional[datetime]
    team_id: Optional[int]
    status: StatusDTO


