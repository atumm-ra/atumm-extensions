from builtins import BaseException
from typing import Any, List, Optional, Type

from atumm.core.types import AsyncContextManager
from beanie import init_beanie
from beanie.odm.documents import Document
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .transformer import BeanieTransformer
from .di import AsyncMotorClientProvider


async def init_my_beanie(
    client: AsyncIOMotorClient, db_name: str, documents: List[Document]
) -> AsyncIOMotorDatabase:
    db = client[db_name]

    await init_beanie(db, document_models=documents)
    return db


class BeanieLifespan(AsyncContextManager):
    def __init__(
        self, client: AsyncIOMotorClient, db_name: str, documents: List[Document]
    ):
        self.beanie_client = client
        self.db_name = db_name
        self.documents = documents

    async def __aenter__(self) -> AsyncIOMotorDatabase:
        return await init_my_beanie(
            client=self.beanie_client, db_name=self.db_name, documents=self.documents
        )

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Any,
    ) -> None:
        await self.beanie_client.close()


__all__ = [
    'BeanieTransformer'
    'AsyncMotorClientProvider',
    'BeanieLifespan',
    'init_my_beanie',
]