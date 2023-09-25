from atumm.extensions.alchemy import AsyncSessionFactory
from atumm.extensions.config import Config
from injector import Module, provider, singleton
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class AlchemyProvider(Module):
    @provider
    @singleton
    def provide_engine(self, config: Config) -> AsyncEngine:
        return create_async_engine(config.DB_URL, echo=config.DEBUG)

    @provider
    @singleton
    def provide_async_session_factory(self, engine: AsyncEngine) -> AsyncSessionFactory:
        return AsyncSessionFactory(engine)
