from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserDM:
    id: int
    name: str
    email: str
    hashed_password: str
    created_at: datetime
    image: Optional[str]
    yandex_id: Optional[int]