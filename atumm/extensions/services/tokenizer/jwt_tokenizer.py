from datetime import datetime, timedelta
from typing import Any, Mapping

import jwt
from atumm.extensions.services.tokenizer.base import BaseTokenizer
from atumm.extensions.services.tokenizer.exceptions import (
    DecodeTokenException,
    ExpiredTokenException,
)


class JWTTokenizer(BaseTokenizer):
    def __init__(
        self, secret_key: str, expire_period: int, jwt_algorithm: str = "HS256"
    ):
        self.secret_key = secret_key
        self.expire_period = expire_period
        self.jwt_algorithm = jwt_algorithm
        self.jwt_obj = jwt.PyJWT()
        self.jwt_obj.options["verify_aud"] = False

    def encode(self, payload: dict) -> str:
        token = self.jwt_obj.encode(
            payload={
                **payload,
                "exp": datetime.utcnow() + timedelta(seconds=self.expire_period),
            },
            key=self.secret_key,
            algorithm=self.jwt_algorithm,
        )
        return token

    def decode(self, token: str, verify=True) -> Mapping[str, Any]:
        try:
            return self.jwt_obj.decode(
                jwt=token,
                key=self.secret_key,
                algorithms=[self.jwt_algorithm],
                verify=True,
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException
