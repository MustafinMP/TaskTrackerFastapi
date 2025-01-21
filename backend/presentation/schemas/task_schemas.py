from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateTaskSchema(BaseModel):
    title: str
    description: str
    project_id: int
    deadline: Optional[datetime]
    status_id: Optional[int]
