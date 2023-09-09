from injector import provider, singleton, Module
from motor.motor_asyncio import AsyncIOMotorClient

class AsyncMotorClientProvider(Module):
    @provider
    @singleton
    def provide_async_motor(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(self.__injector__.get(Config).MONGO_URL)