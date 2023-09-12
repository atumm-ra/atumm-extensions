from atumm.core.infra.config import Config
from injector import Module, provider, singleton
from motor.motor_asyncio import AsyncIOMotorClient


class AsyncMotorClientProvider(Module):
    @provider
    @singleton
    def provide_async_motor(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(self.__injector__.get(Config).MONGO_URL)
