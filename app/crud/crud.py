# Sessions will allow you to declare the type of the db
# parameters and have better type checks and completion
# functions.
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload


# Import models (the sqlalchemy models) and schemas (the pydantic schemas)
from app.models import declines
from app.schemas import schemas

def get_decline_by_well(db: AsyncSession, well_id: str):
    """Read a single decline by id"""
    return db.execute(select(declines.Decline).
                      where(declines.Decline.well_id == well_id).
                      options(selectinload(declines.Decline.segments)))

def get_declines(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Read multiple declines"""
    return db.execute(select(declines.Decline).
                      offset(skip).limit(limit).
                      options(selectinload(declines.Decline.segments)))

async def create_decline(db: AsyncSession, decline: schemas.DeclineCreate):
    """Create data, the steps are:
         * Create a sqlalchemy model instance with your data
         * add that instance object to your database
         * commit the changes to the database
         * refresh your instance
    """
    db_decline = declines.Decline(well_id=decline.well_id, created_at=decline.created_at)
    db.add(db_decline)
    await db.commit()
    # Adding ["segments"] to refresh prevents implicit IO Errors
    await db.refresh(db_decline, ["segments"])
    return db_decline

async def create_decline_segment(db: AsyncSession, segment: schemas.SegmentCreate, decline_id: int):
    """Create data, the steps are:
         * Create a sqlalchemy model instance with your data
         * add that instance object to your database
         * commit the changes to the database
         * refresh your instance
    """
    db_decline_segment = declines.Segment(**segment.model_dump(), decline_id=decline_id)
    db.add(db_decline_segment)
    await db.commit()
    # Adding ["segments"] to refresh prevents implicit IO Errors
    await db.refresh(db_decline_segment)
    return db_decline_segment

# def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
#     "Read multiple items"
#     return db.query(models.Item).offset(skip).limit(limit).all()

# def create_user_item(db: AsyncSession, item: schemas.ItemCreate, user_id: int):
#     # Instead of passing each of the keyword args to Item and reading each
#     # one from the pydantic model, we are generating a dict item.model_dump()
#     # and then psssing the dicts key-value pairs as the keyword args to the
#     # sqlalchemy Item, with Item(**item.model_dump()) and then we pass the
#     # extra keyword arg owner_id that is not provided by the pydantic model.
#     db_item = models.Item(**item.model_dump(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

