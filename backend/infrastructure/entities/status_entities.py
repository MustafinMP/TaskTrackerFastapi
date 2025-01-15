from dataclasses import dataclass
from typing import Optional


@dataclass
class StatusDM:
    id: int
    name: str
    color_tag: Optional[str]
