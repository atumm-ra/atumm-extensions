from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession


class AsyncSessionFactory:
    def __init__(self, engine: AsyncEngine):
        self._sessionmaker = sessionmaker(
            bind=engine, expire_on_commit=False, class_=AsyncSession
        )

    def new_session(self) -> AsyncSession:
        return self._sessionmaker()
