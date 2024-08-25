from typing import Optional, List
from sqlalchemy import TIMESTAMP, ForeignKey, String, DECIMAL, NUMERIC
from sqlalchemy.orm import Mapped, mapped_column, relationship 

from app.db.database import Base
from datetime import datetime, timezone

# Note there are differences between asyncpg and psycopg
# in how you define your models. The type_ below is required
# for asyncpg not psycopg

class Decline(Base):
    __tablename__ = "decline"
    __table_args__ = {"schema": "public"}

    decline_id : Mapped[int] = mapped_column(primary_key=True)
    well_id : Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=False),
        default=datetime.now(timezone.utc))
    
    segments: Mapped[List["Segment"]] =  relationship(back_populates="decline")
    
class Segment(Base):
    __tablename__ = "segment"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(primary_key=True)
    fluid: Mapped[str] = mapped_column(nullable=True)
    segment: Mapped[int] = mapped_column(nullable=True)
    date_start: Mapped[datetime] = mapped_column(nullable=True)
    date_end: Mapped[datetime] = mapped_column(nullable=True)
    rate_start: Mapped[float] = mapped_column(NUMERIC)
    decline_rate: Mapped[float] = mapped_column(DECIMAL(6,3))
    exponent: Mapped[Optional[float]] = mapped_column(DECIMAL(5,5))
    decline_id: Mapped[int] = mapped_column(ForeignKey("public.decline.decline_id"))

    decline: Mapped["Decline"] = relationship(back_populates="segments")
