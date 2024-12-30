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
    creator_id: int
    team_id: int
    created_date: datetime
    deadline: Optional[datetime]
    status: StatusDTO


@dataclass
class CreateTaskDM:
    name: str
    description: str
    creator_id: int
    team_id: int
    deadline: Optional[datetime]
    status_id: Optional[int]


@dataclass
class UpdateTaskDM:
    id: int
    name: Optional[str]
    description: Optional[str]
    status_id: Optional[int]
    # deadline: Optional[datetime]



@dataclass
class TaskToTagRelationDM:
    task_id: int
    tag_id: int
