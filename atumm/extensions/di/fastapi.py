from atumm.core.infra.config import Config
from atumm.extensions.fastapi.middlewares.authentication import AuthBackend
from injector import Module, provider, singleton
from starlette.authentication import AuthenticationBackend


class AuthBackendProvider(Module):
    @provider
    @singleton
    def provide_auth_backend(self) -> AuthenticationBackend:
        config = self.__injector__.get(Config)
        return AuthBackend(
            jwt_secret_key=config.JWT_SECRET_KEY, jwt_algorithm=config.JWT_ALGORITHM
        )
