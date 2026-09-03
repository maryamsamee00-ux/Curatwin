from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..models.user import User
from ..models.wellness import WellnessData
from ..schemas.wellness import WellnessDataCreate, WellnessDataResponse
from ..middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/wellness", tags=["wellness"])

@router.post("/telemetry", response_model=WellnessDataResponse)
def ingest_telemetry(data: WellnessDataCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = WellnessData(
        user_id=user.id,
        ppg_hrv=data.ppg_hrv,
        gsr_amplitude=data.gsr_amplitude,
        skin_temp=data.skin_temp,
        imu_activity=data.imu_activity,
        heart_rate=data.heart_rate,
        source=data.source
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/telemetry", response_model=List[WellnessDataResponse])
def get_telemetry(days: int = 7, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=days)
    records = db.query(WellnessData).filter(
        WellnessData.user_id == user.id,
        WellnessData.timestamp >= since
    ).order_by(WellnessData.timestamp.desc()).limit(100).all()
    return records

@router.get("/telemetry/latest", response_model=WellnessDataResponse)
def get_latest_telemetry(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.query(WellnessData).filter(
        WellnessData.user_id == user.id
    ).order_by(WellnessData.timestamp.desc()).first()
    if not record:
        raise HTTPException(status_code=404, detail="No telemetry data found. Connect your wearable to begin personalized wellness tracking.")
    return record
