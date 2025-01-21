# from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CreateTaskDM:
    title: str
    description: str
    creator_id: int
    project_id: int
    deadline: Optional[datetime]
    status_id: Optional[int]


@dataclass
class TaskDM:
    id: int
    title: str
    description: str
    project_id: int
    creator_id: int
    created_date: datetime
    deadline: Optional[datetime]
    status_id: Optional[int]


@dataclass
class UpdateTaskDM:
    id: int
    title: Optional[str]
    description: Optional[str]
    status_id: Optional[int]
    deadline: Optional[datetime]


@dataclass
class TaskToTagRelationDM:
    task_id: int
    tag_id: int


@dataclass
class TagDM:
    id: int
    name: str
