from dataclasses import dataclass
from typing import Optional


@dataclass
class StatusDTO:
    id: int
    name: str
    color_tag: Optional[str]