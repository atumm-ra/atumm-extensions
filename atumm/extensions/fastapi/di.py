from atumm.extensions.fastapi.middlewares.authentication import AuthBackend
from atumm.services.user.infra.auth.tokenizer import Tokenizer
from injector import Module, provider, singleton
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.authentication import AuthenticationBackend


class AuthenticationBackendProvider(Module):
    @provider
    @singleton
    def provide(self, tokenizer: Tokenizer) -> AuthenticationBackend:
        return AuthBackend(tokenizer)
