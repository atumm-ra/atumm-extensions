from atumm.core.entrypoints.rest.responses import map_exception_to_response
from atumm.core.exceptions import ErrorStatus, ExceptionDetail, RuntimeException
from atumm.core.infra.config import Config
from atumm.extensions.buti.keys import AtummContainerKeys
from atumm.extensions.fastapi.base import ProductionWebApp
from atumm.extensions.fastapi.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    ResponseLogMiddleware,
)
from buti import BootableComponent, ButiStore
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from starlette.authentication import AuthenticationBackend
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class FastAPIComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        config: Config = store.get(AtummContainerKeys.config)
        app: FastAPI = ProductionWebApp(config).app
        store.set(AtummContainerKeys.app, app)
        app.user_middleware = self.make_middlewares(
            store.get(AtummContainerKeys.injector).get(AuthenticationBackend)
        )
        self.register_exception_listeners(app)

    def make_middlewares(self, auth_backend: AuthenticationBackend):
        return [
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            ),
            Middleware(AuthenticationMiddleware, backend=auth_backend),
            Middleware(ResponseLogMiddleware),
        ]

    def register_exception_listeners(self, app):
        @app.exception_handler(RuntimeException)
        async def handle_runtime_exception(
            request: Request, exception: RuntimeException
        ):
            code, response = map_exception_to_response(exception)
            return JSONResponse(content=response.dict(), status_code=code)

        @app.exception_handler(AuthJWTException)
        async def on_auth_error(request: Request, exc: AuthJWTException):
            status_code, message = 401, exc.message
            status_code, response = map_exception_to_response(
                RuntimeException(
                    code=status_code,
                    message=message,
                    status=ErrorStatus.TOKEN_ERROR,
                    details=[
                        ExceptionDetail(type=exc.__class__.__name__, reason=message)
                    ],
                )
            )
            return JSONResponse(response.dict(), status_code=401)

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(
            request: Request, exc: RequestValidationError
        ):
            details = []
            for error in exc.errors():
                details.append(
                    ExceptionDetail(
                        type=error["type"],
                        reason=error["msg"],
                        metadata={"location": ".".join(map(str, error["loc"]))},
                    )
                )
            api_exception = RuntimeException(
                code=400,
                message="Validation error",
                status=ErrorStatus.VALIDATION_ERROR,
                details=details,
            )
            code, response = map_exception_to_response(api_exception)
            return JSONResponse(response.dict(), status_code=code)


class AuthJWTComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        config: Config = store.get(AtummContainerKeys.config)

        class Settings(BaseModel):
            authjwt_secret_key: str = config.JWT_SECRET_KEY
            authjwt_algorithm: str = config.JWT_ALGORITHM

        # callback to get your configuration
        @AuthJWT.load_config
        def get_jwt_config():
            return Settings()
