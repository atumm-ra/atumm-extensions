from atumm.extensions.fastapi.middlewares.authentication import AuthBackend
from injector import Module, provider, singleton
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.authentication import AuthenticationBackend
from atumm.extensions.services.tokenizer.base import BaseTokenizer


class AuthenticationBackendProvider(Module):
    @provider
    @singleton
    def provide(self, tokenizer: BaseTokenizer) -> AuthenticationBackend:
        return AuthBackend(tokenizer)
