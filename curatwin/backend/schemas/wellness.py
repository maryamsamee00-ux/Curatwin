from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WellnessDataCreate(BaseModel):
    ppg_hrv: float = 0.0
    gsr_amplitude: float = 0.0
    skin_temp: float = 36.5
    imu_activity: float = 0.0
    heart_rate: float = 0.0
    source: str = "simulator"


class WellnessDataResponse(BaseModel):
    id: int
    user_id: int
    timestamp: Optional[datetime] = None
    ppg_hrv: float
    gsr_amplitude: float
    skin_temp: float
    imu_activity: float
    heart_rate: float
    source: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
