from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Create pydantic models DeclineBase and SegmentBase to
# have common attributes while creating or reading data.
class SegmentBase(BaseModel):
    # The following replaces orm_mode.  It reads the
    # instance attributes corresponding to the model
    # field names.
    model_config = ConfigDict(from_attributes=True)
    
    fluid: str
    segment: int
    date_start: datetime
    date_end: datetime
    rate_start: float
    decline_rate: float
    exponent: float | None = None

    
class SegmentCreate(SegmentBase):
    pass

class Segment(SegmentBase):
    id: int
    decline_id: int

class DeclineBase(BaseModel):
    # The following replaces orm_mode
    model_config = ConfigDict(from_attributes=True)


class DeclineCreate(DeclineBase):
    well_id: str

    
class Decline(DeclineCreate):
    decline_id: int
    created_at: datetime
    segments: list[Segment] = []
    
