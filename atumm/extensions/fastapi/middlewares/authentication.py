from typing import Optional, Tuple

import jwt
from atumm.extensions.fastapi.schemas import CurrentUser
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection


class AuthBackend(AuthenticationBackend):
    def __init__(self, jwt_secret_key: str, jwt_algorithm: str) -> None:
        super().__init__()
        self.jwt_secret_key = jwt_secret_key
        self.jwt_algorithm = jwt_algorithm

    async def authenticate(
        self, conn: HTTPConnection
    ) -> Tuple[bool, Optional[CurrentUser]]:
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            scheme, credentials = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not credentials:
            return False, current_user

        try:
            payload = jwt.decode(
                credentials,
                self.jwt_secret_key,
                algorithms=[self.jwt_algorithm],
            )
            current_user.email = payload.get("sub")
            current_user.id = payload.get("user_id")
        except jwt.exceptions.PyJWTError:
            return False, current_user

        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
