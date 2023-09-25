from atumm.extensions.config import Config
from injector import Module, provider, singleton
from motor.motor_asyncio import AsyncIOMotorClient


class AsyncMotorClientProvider(Module):
    @provider
    @singleton
    def provide_async_motor(self, config: Config) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(config.MONGO_URL)
