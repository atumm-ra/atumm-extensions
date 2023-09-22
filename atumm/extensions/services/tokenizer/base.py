from abc import ABC, abstractmethod
from typing import Any, Mapping

class TokenizerConfig:
    def __init__(self, expire_period: int = 43200, jwt_algorithm: str = "HS256"):
        self.expire_period = expire_period
        self.jwt_algorithm = jwt_algorithm

class BaseTokenizer(ABC):

    @abstractmethod
    def encode(self, payload: dict) -> str:
        pass

    @abstractmethod
    def decode(self, token: str, verify=True) -> Mapping[str, Any]:
        pass