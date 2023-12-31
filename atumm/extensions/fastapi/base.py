from atumm.extensions.config import Config
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
            swagger_ui_parameters={
                "swagger_js_url": "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.0.0/swagger-ui-bundle.js",
                "swagger_css_url": "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.0.0/swagger-ui.css",
            },
        )


class TestWebApp(BaseWebApp):
    pass


class ProductionWebApp(BaseWebApp):
    pass
