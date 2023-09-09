import os
from functools import lru_cache

from atumm.core.infra.config import Config


class AppConfig(Config):
    APP_HOST: str
    APP_PORT: int

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    PASSWORD_KEY: str

    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASS: str
    MONGO_DB: str
    MONGO_URL: str


class DevelopmentConfig(AppConfig):
    pass


class LocalConfig(AppConfig):
    pass


class ProductionConfig(AppConfig):
    pass


class TestConfig(AppConfig):
    pass



def get_config() -> Config:
    env = os.environ['STAGE']
    
    match env:
        case 'local':
            return LocalConfig(_env_file=".env")
        case 'test':
            return TestConfig(_env_file=".env.test")
        case 'dev':
            return DevelopmentConfig(_env_file=".env")
        case 'prod':
            return ProductionConfig(_env_file=".env")
        case _:
            raise ValueError("invalid '{env}' stage")
