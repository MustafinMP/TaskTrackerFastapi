import uuid
from time import time

from fastapi import Cookie
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from presentation.schemas.cookie import CookieSession

COOKIE_SESSION_ID_KEY = 'session-id'


class CookieManager:
    def __init__(self) -> None:
        self._cookies: dict[str, CookieSession] = {}

    async def set_cookie(self, response: Response, user_id: int) -> None:
        session_id = uuid.uuid4().hex  # generate_code
        response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
        cookie = CookieSession(user_id=user_id, login_at=int(time()))
        self._cookies[session_id] = cookie

    def get_session_data(self, session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)) -> CookieSession:
        if session_id not in self._cookies:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return self._cookies[session_id]

    async def get_current_user_id(self, session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)) -> int:
        if session_id not in self._cookies:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return self._cookies[session_id].user_id
