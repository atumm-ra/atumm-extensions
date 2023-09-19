from sqlalchemy.orm.decl_api import DeclarativeBase

from .di import AlchemyProvider
from .session import AsyncSessionFactory


class Base(DeclarativeBase):
    pass


__all__ = [
    "Base",
    "AsyncSessionFactory",
    "AlchemyProvider",
]
