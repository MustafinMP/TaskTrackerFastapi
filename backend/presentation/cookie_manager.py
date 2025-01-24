import uuid
from time import time

from fastapi import Cookie
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from presentation.schemas.cookie import CookieSession

COOKIE_SESSION_ID_KEY = 'session-id'


class CookieManager:
    """Главное назначение этого класса - установка и хранение куки сессий. Временно реализован в виде словаря, однако
    в будущем планируется изменить реализацию с другим хранилищем, либо, по аналогии с фласком, сделать хранение
    зашифрованного куки на клиенте без хранения на бекенде.

    """
    _cookies: dict[str, CookieSession] = {}

    def __init__(self) -> None:
        ...

    def set_cookie(self, response: Response, user_id: int) -> None:
        session_id = uuid.uuid4().hex  # generate_code
        cookie = CookieSession(user_id=int(user_id), login_at=int(time()))
        self._cookies[session_id] = cookie
        response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)

    def get_session_data(self, session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)) -> CookieSession:
        if session_id not in self._cookies:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return self._cookies[session_id]

    def get_current_user_id(self, session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)) -> int | None:
        if session_id not in self._cookies:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return self._cookies[session_id].user_id
