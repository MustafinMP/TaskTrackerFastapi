from dataclasses import dataclass


@dataclass
class CookieSession:
    user_id: str
    login_at: int
