from dataclasses import dataclass


@dataclass
class CookieSessionDTO:
    user_id: str
    login_at: int
