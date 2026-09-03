from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CycleRecordCreate(BaseModel):
    cycle_start: str
    cycle_length: int = 28
    symptoms: str = ""
    mood_observations: str = ""
    physical_discomfort: str = ""
    temperature_summary: str = ""


class CycleRecordUpdate(BaseModel):
    cycle_end: Optional[str] = None
    symptoms: Optional[str] = None
    mood_observations: Optional[str] = None
    physical_discomfort: Optional[str] = None
    temperature_summary: Optional[str] = None


class CycleRecordResponse(BaseModel):
    id: int
    user_id: int
    cycle_start: datetime
    cycle_end: Optional[datetime] = None
    cycle_length: int
    symptoms: str
    mood_observations: str
    physical_discomfort: str
    estimated_phase: str
    temperature_summary: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
