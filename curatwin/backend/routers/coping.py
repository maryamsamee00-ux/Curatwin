from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..models.user import User
from ..models.coping import CopingIntervention
from ..models.stress import StressPrediction
from ..models.cycle import CycleRecord
from ..schemas.coping import CopingResponse
from ..middleware.auth_middleware import get_current_user
from ..services.coping_engine import get_recommendations, get_library_categories
from ..services.cycle_service import estimate_phase

router = APIRouter(prefix="/api/coping", tags=["coping"])

@router.get("/recommendations")
def get_recs(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    latest_stress = db.query(StressPrediction).filter(
        StressPrediction.user_id == user.id
    ).order_by(StressPrediction.timestamp.desc()).first()
    
    stress_level = latest_stress.stress_level if latest_stress else "moderate"
    
    latest_cycle = db.query(CycleRecord).filter(
        CycleRecord.user_id == user.id
    ).order_by(CycleRecord.cycle_start.desc()).first()
    
    cycle_phase = ""
    if latest_cycle:
        cycle_phase = estimate_phase(latest_cycle.cycle_start, latest_cycle.cycle_length)
    
    recs = get_recommendations(stress_level, cycle_phase, count=3)
    
    saved = []
    for rec in recs:
        intervention = CopingIntervention(
            user_id=user.id,
            intervention_type=rec["intervention_type"],
            category=rec["category"],
            title=rec["title"],
            recommendation=rec["recommendation"],
            trigger=f"stress:{stress_level}"
        )
        db.add(intervention)
        saved.append(intervention)
    
    db.commit()
    return {"recommendations": recs, "stress_level": stress_level}

@router.get("/library")
def get_library():
    return {"categories": get_library_categories()}

@router.get("/history", response_model=List[CopingResponse])
def get_history(days: int = 7, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=days)
    records = db.query(CopingIntervention).filter(
        CopingIntervention.user_id == user.id,
        CopingIntervention.created_at >= since
    ).order_by(CopingIntervention.created_at.desc()).limit(20).all()
    return records
