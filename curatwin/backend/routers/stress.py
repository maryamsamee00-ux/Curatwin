from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..models.user import User
from ..models.stress import StressPrediction
from ..schemas.stress import StressPredictionResponse, TelemetryRequest
from ..middleware.auth_middleware import get_current_user
from ..services.stress_engine import predict_stress

router = APIRouter(prefix="/api/stress", tags=["stress"])

@router.post("/predict", response_model=StressPredictionResponse)
def predict(data: TelemetryRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        level, confidence, version, features = predict_stress(
            data.ppg_hrv, data.gsr_amplitude, data.skin_temp, data.imu_activity, data.self_report_stress
        )
        prediction = StressPrediction(
            user_id=user.id,
            stress_level=level,
            confidence=confidence,
            model_version=version,
            features_used=features
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to generate stress prediction at this time. Please try again later.")

@router.get("/history", response_model=List[StressPredictionResponse])
def get_history(days: int = 7, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=days)
    records = db.query(StressPrediction).filter(
        StressPrediction.user_id == user.id,
        StressPrediction.timestamp >= since
    ).order_by(StressPrediction.timestamp.desc()).limit(50).all()
    return records

@router.get("/current")
def get_current_stress(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.query(StressPrediction).filter(
        StressPrediction.user_id == user.id
    ).order_by(StressPrediction.timestamp.desc()).first()
    if not record:
        return {"stress_level": "unknown", "confidence": 0, "message": "No stress data yet. Submit telemetry to get your first prediction."}
    return {"stress_level": record.stress_level, "confidence": record.confidence, "timestamp": record.timestamp.isoformat()}
