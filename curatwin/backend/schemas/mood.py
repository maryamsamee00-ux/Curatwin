from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MoodCheckinCreate(BaseModel):
    mood: float = 0.5
    perceived_stress: float = 0.5
    sleep_quality: float = 0.5
    energy_level: float = 0.5
    symptoms: str = ""
    menstrual_symptoms: str = ""
    notes: str = ""


class MoodCheckinResponse(BaseModel):
    id: int
    user_id: int
    mood: float
    perceived_stress: float
    sleep_quality: float
    energy_level: float
    symptoms: str
    menstrual_symptoms: str
    notes: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
