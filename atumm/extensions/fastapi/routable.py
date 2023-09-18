import inspect
from abc import ABC

from fastapi import APIRouter, Request
from starlette.routing import Route, WebSocketRoute


class Routable(ABC):
    """
    Provides class-based routing to fastapi
    thanks to: Josh Lowery (@loweryjk) for providing this base class

    example:
        from atumm.extensions.fastapi.routable import Routable, bind_router
        from fastapi import Response
        from fastapi.routing import APIRouter

        router = APIRouter()


        @bind_router(router)
        class HealthRouter(Routable):
            @router.get("/health")
            async def health(self):
                return Response(status_code=200)

        app = FastAPI()
        app.include_router(HealthRouter().router)
    """

    router: APIRouter

    def _bind_routes(self, router: APIRouter) -> APIRouter:
        """Bind routes defined in the router to class methods."""
        methods = set(
            method
            for _, method in inspect.getmembers(self.__class__, inspect.isfunction)
        )
        routes = [
            route
            for route in router.routes
            if isinstance(route, (Route, WebSocketRoute)) and route.endpoint in methods
        ]
        for route in routes:
            route.endpoint = route.endpoint.__get__(self, self.__class__)
        return router


def bind_router(router: APIRouter):
    """Decorator to bind routes to class methods."""

    def decorator(cls):
        class NewCls(cls, Routable):
            def __init__(self, *args, **kwargs):
                self.router = self._bind_routes(router)
                super(NewCls, self).__init__(*args, **kwargs)

        return NewCls

    return decorator
