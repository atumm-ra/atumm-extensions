from atumm.extensions.tokenizer.base import BaseTokenizer
from datetime import datetime, timedelta


class PasetoTokenizer(BaseTokenizer):

    def __init__(self, secret_key: str, expire_period: int):
        self.secret_key = secret_key
        self.expire_period = expire_period

    def encode(self, payload: dict) -> str:
        expiration = datetime.utcnow() + timedelta(seconds=self.expire_period)
        payload["exp"] = expiration.strftime('%Y-%m-%dT%H:%M:%S')
        return pyseto.encode(self.secret_key, payload, version="v4", purpose="local")

    def decode(self, token: str, verify=True) -> Mapping[str, Any]:
        decoded = pyseto.decode(self.secret_key, token, version="v4", purpose="local")
        return decoded.get("payload")

