from typing import List

from atumm.core.infra.config import Config
from fastapi import FastAPI


class BaseWebApp:
    def __init__(self, config: Config):
        self.config = config
        self.app = FastAPI(
            title=self.config.API_TITLE,
            description=self.config.API_DESCRIPTION,
            version=self.config.API_VERSION,
            docs_url=None if self.config.STAGE == "prod" else "/docs",
            redoc_url=None if self.config.STAGE == "prod" else "/redoc",
        )


class TestWebApp(BaseWebApp):
    pass


class ProductionWebApp(BaseWebApp):
    pass
