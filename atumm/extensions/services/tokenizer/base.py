from abc import ABC, abstractmethod
from typing import Any, Mapping


class BaseTokenizer(ABC):
    @abstractmethod
    def encode(self, payload: dict) -> str:
        pass

    @abstractmethod
    def decode(self, token: str, verify=True) -> Mapping[str, Any]:
        pass
