from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    email: str
    created_at: datetime


class ProfileResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    user_id: int
    age_range: str
    university: str
    baseline_stress: float
    baseline_mood: float
    baseline_sleep: float
    onboarding_complete: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProfileUpdate(BaseModel):
    age_range: Optional[str] = None
    university: Optional[str] = None
    baseline_stress: Optional[float] = None
    baseline_mood: Optional[float] = None
    baseline_sleep: Optional[float] = None
    onboarding_complete: Optional[int] = None
