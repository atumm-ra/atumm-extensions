from atumm.services.user.dataproviders.beanie.models import User
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


# todo: refactor - pass models, and make a model collector
async def init_my_beanie(
    client: AsyncIOMotorClient, db_name: str
) -> AsyncIOMotorDatabase:
    db = client[db_name]

    await init_beanie(db, document_models=[User])
    return db
