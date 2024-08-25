from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from app.db.database import get_db_session
from app.schemas import schemas

from app.crud import crud

# get_db_session from database.py will become our fundamental
# db interface across the app.  First we turn it into
# a dependency:
DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

router = APIRouter(
    prefix="/declines",
    tags=['Declines']
)

@router.post("/", response_model=schemas.Decline)
async def create_decline(decline: schemas.DeclineCreate, db: DBSessionDep):
    db_decline = await crud.get_decline_by_well(db, well_id=decline.well_id)
    # if db_decline:
    #     raise HTTPException(status_code=400, detail="Decline already registered")
    result = await crud.create_decline(db=db, decline=decline)
    return result

@router.get("/", response_model=list[schemas.Decline])
async def read_declines(db: DBSessionDep,skip: int = 0, limit: int = 100):
    results = await crud.get_declines(db, skip=skip, limit=limit)
    declines = results.scalars().all()
    return declines

@router.post("/{decline_id}/segments/", response_model=schemas.Segment)
async def create_segment_for_decline(
        db: DBSessionDep,
        decline_id: int,
        segment: schemas.SegmentCreate
        ):
    segment = await crud.create_decline_segment(db=db, segment=segment, decline_id=decline_id)
    return segment
