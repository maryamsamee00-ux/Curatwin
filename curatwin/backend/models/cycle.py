from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from ..database import Base


class CycleRecord(Base):
    __tablename__ = "cycle_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    cycle_start = Column(DateTime, nullable=False)
    cycle_end = Column(DateTime, nullable=True)
    cycle_length = Column(Integer, default=28)
    symptoms = Column(Text, default="")
    mood_observations = Column(Text, default="")
    physical_discomfort = Column(Text, default="")
    estimated_phase = Column(String(50), default="")
    temperature_summary = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
