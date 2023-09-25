from datetime import datetime, timedelta
from typing import Any, Mapping

from pyseto.versions.v4 import V4Local
from atumm.extensions.services.tokenizer.base import BaseTokenizer
from pyseto.key import Key
import pyseto
import pyseto.exceptions
import json
from atumm.extensions.services.tokenizer.exceptions import ExpiredTokenException,\
    DecodeTokenException


class PasetoTokenizer(BaseTokenizer):

    def __init__(self, secret_key: str, expire_period: int):
        self.paseto_key = Key.new(version=4, purpose="local", key=secret_key.encode())
        self.expire_period = expire_period

    def encode(self, payload: dict) -> str:
        expiration = datetime.utcnow() + timedelta(seconds=self.expire_period)
        payload["exp"] = expiration.strftime("%Y-%m-%dT%H:%M:%S")
        return pyseto.encode(key=self.paseto_key, payload=payload).decode('utf-8')

    def decode(self, token: str, verify=True) -> Mapping[str, Any]:
        try:
            decoded = pyseto.decode(keys=[self.paseto_key], token=token)
            payload_str = decoded.payload.decode('utf-8')
            payload = json.loads(payload_str)

            # Check token expiration
            self._has_expired(payload)

            return payload

        except ValueError as e:
            raise DecodeTokenException
    
    def _has_expired(self, payload):
        expiration = datetime.strptime(payload["exp"], "%Y-%m-%dT%H:%M:%S")
        if datetime.utcnow() > expiration:
            raise ExpiredTokenException
