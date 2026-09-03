from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..models.user import User
from ..models.mood import MoodCheckin
from ..schemas.mood import MoodCheckinCreate, MoodCheckinResponse
from ..middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/mood", tags=["mood"])

@router.post("/checkin", response_model=MoodCheckinResponse)
def create_checkin(data: MoodCheckinCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    checkin = MoodCheckin(
        user_id=user.id,
        mood=data.mood,
        perceived_stress=data.perceived_stress,
        sleep_quality=data.sleep_quality,
        energy_level=data.energy_level,
        symptoms=data.symptoms,
        menstrual_symptoms=data.menstrual_symptoms,
        notes=data.notes
    )
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin

@router.get("/checkins", response_model=List[MoodCheckinResponse])
def get_checkins(days: int = 30, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=days)
    records = db.query(MoodCheckin).filter(
        MoodCheckin.user_id == user.id,
        MoodCheckin.created_at >= since
    ).order_by(MoodCheckin.created_at.desc()).limit(50).all()
    return records

@router.get("/checkins/latest", response_model=MoodCheckinResponse)
def get_latest_checkin(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.query(MoodCheckin).filter(
        MoodCheckin.user_id == user.id
    ).order_by(MoodCheckin.created_at.desc()).first()
    if not record:
        raise HTTPException(status_code=404, detail="Complete your first private wellness check-in.")
    return record
