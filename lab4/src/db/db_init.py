from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

import src.db.models


async def create_models(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(src.db.models.Base.metadata.create_all)


async def init_db(engine: AsyncEngine):
    await create_models(engine)
