from app.models import declines
from sqlalchemy import DDL, event

async def create_db_and_tables(engine):
    async with engine.connect() as conn:
        # Maybe I should use alembic instead of all this
        event.listen(declines.Base.metadata, 'before_create', DDL("DROP SCHEMA IF EXISTS ab_decline_raw"))
        event.listen(declines.Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS ab_decline_raw"))
        await conn.run_sync(declines.Base.metadata.create_all)
    # yield
    # # Teardown
    # await engine.close()

async def drop_db_and_tables(engine):
    async with engine.connect() as conn:
       await conn.run_sync(declines.Base.metadata.drop_all)
    yield
    # Teardown
    await engine.close()
    
    
async def recreate_db_and_tables(engine):
    async with engine.connect() as conn:
        await conn.run_sync(declines.Base.metadata.drop_all)
        await conn.run_sync(declines.Base.metadata.create_all)
    yield
    # Teardown
    await engine.close()
    
