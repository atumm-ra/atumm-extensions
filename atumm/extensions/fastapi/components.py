from atumm.core.entrypoints.rest.responses import map_exception_to_response
from atumm.core.exceptions import ErrorStatus, ExceptionDetail, RuntimeException
from atumm.extensions.buti.keys import AtummContainerKeys
from atumm.extensions.config import Config
from atumm.extensions.di.resolver import DependencyResolver
from atumm.extensions.fastapi.base import ProductionWebApp
from atumm.extensions.fastapi.middlewares import (
    AuthenticationMiddleware,
    ResponseLogMiddleware,
)
from buti import BootableComponent, ButiStore
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from injector import Injector
from pydantic import ValidationError
from starlette.authentication import AuthenticationBackend
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class FastAPIComponent(BootableComponent):
    def boot(self, store: ButiStore) -> None:
        config: Config = store.get(AtummContainerKeys.config)
        app: FastAPI = ProductionWebApp(config).app
        injector: Injector = store.get(AtummContainerKeys.injector)
        store.set(AtummContainerKeys.app, app)

        DependencyResolver.set_resolver(injector)

        app.user_middleware = self.make_middlewares(injector.get(AuthenticationBackend))
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

        @app.exception_handler(ValidationError)
        async def pydantic_validation_exception_handler(
            request: Request, exc: ValidationError
        ):
            details = []
            for error in exc.errors():
                # Extract additional context from the error
                ctx = error.get("ctx", {})
                details.append(
                    ExceptionDetail(
                        type=ctx.get("type", error["type"]),
                        reason=error["msg"],
                        metadata={
                            "location": ".".join(map(str, error["loc"])),
                            "input_value": str(ctx.get("input_value", "N/A")),
                            "input_type": str(ctx.get("input_type", "N/A")),
                        },
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
