from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TelemetryRequest(BaseModel):
    ppg_hrv: float = 50.0
    gsr_amplitude: float = 5.0
    skin_temp: float = 36.5
    imu_activity: float = 0.3
    self_report_stress: float = 0.5


class StressPredictionResponse(BaseModel):
    model_config = {"protected_namespaces": (), "from_attributes": True}

    id: int
    user_id: int
    timestamp: Optional[datetime] = None
    stress_level: str
    confidence: float
    model_version: str
    features_used: str
    created_at: Optional[datetime] = None
