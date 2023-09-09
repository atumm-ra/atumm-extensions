from typing import List

from fastapi import FastAPI

from thisapp.config import Config, get_config

class BaseWebApp:
    def __init__(self, config: Config):
        self.config = config
        self.app = FastAPI(
            title="Atumm API",
            description="",
            version="1.0.0",
            docs_url=None if self.config.STAGE == "prod" else "/docs",
            redoc_url=None if self.config.STAGE == "prod" else "/redoc",
        )

class TestWebApp(BaseWebApp):
    pass


class ProductionWebApp(BaseWebApp):
    pass

