from typing import Callable, Optional, Tuple

import jwt
from atumm.core.exceptions import RuntimeException
from atumm.extensions.fastapi.schemas import CurrentUser
from atumm.services.user.infra.auth.tokenizer import Tokenizer
from injector import inject
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection, Request


class AuthBackend(AuthenticationBackend):
    @inject
    def __init__(self, tokenizer: Tokenizer) -> None:
        self.tokenizer = tokenizer

    async def authenticate(
        self, conn: HTTPConnection
    ) -> Tuple[bool, Optional[CurrentUser]]:
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            scheme, access_token = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not access_token:
            return False, current_user

        try:
            payload = self.tokenizer.decode(access_token, True)
            current_user.email = payload.get("sub")
            current_user.id = payload.get("user_id")
        except jwt.exceptions.PyJWTError:
            return False, current_user

        return True, current_user

    async def _resume(self, request, call_next):
        response = await call_next(request)

        return response

    async def __call__(self, request: Request, call_next: Callable):
        authorization: str = request.headers.get("Authorization")

        if not authorization:
            return self._resume(request, call_next)

        parts = authorization.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return self._resume(request, call_next)

        access_token = parts[1]
        if not access_token:
            return self._resume(request, call_next)

        try:
            payload = self.tokenizer.decode(access_token, True)
            current_user = CurrentUser()
            current_user.email = payload.get("sub")
            current_user.id = payload.get("user_id")
            request.user = current_user
        except RuntimeException:
            return self._resume(request, call_next)


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
