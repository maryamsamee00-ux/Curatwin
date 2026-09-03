from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models.user import User
from ..models.cycle import CycleRecord
from ..schemas.cycle import CycleRecordCreate, CycleRecordUpdate, CycleRecordResponse
from ..middleware.auth_middleware import get_current_user
from ..services.cycle_service import estimate_phase, get_cycle_insights

router = APIRouter(prefix="/api/cycle", tags=["cycle"])

@router.post("/records", response_model=CycleRecordResponse)
def create_record(data: CycleRecordCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        cycle_start = datetime.fromisoformat(data.cycle_start)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format (YYYY-MM-DD).")
    
    phase = estimate_phase(cycle_start, data.cycle_length)
    
    record = CycleRecord(
        user_id=user.id,
        cycle_start=cycle_start,
        cycle_length=data.cycle_length,
        symptoms=data.symptoms,
        mood_observations=data.mood_observations,
        physical_discomfort=data.physical_discomfort,
        estimated_phase=phase,
        temperature_summary=data.temperature_summary
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/records", response_model=List[CycleRecordResponse])
def get_records(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(CycleRecord).filter(
        CycleRecord.user_id == user.id
    ).order_by(CycleRecord.cycle_start.desc()).limit(20).all()
    return records

@router.put("/records/{record_id}", response_model=CycleRecordResponse)
def update_record(record_id: int, data: CycleRecordUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.query(CycleRecord).filter(CycleRecord.id == record_id, CycleRecord.user_id == user.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Cycle record not found.")
    
    update_data = data.model_dump(exclude_unset=True)
    if "cycle_end" in update_data and update_data["cycle_end"]:
        try:
            update_data["cycle_end"] = datetime.fromisoformat(update_data["cycle_end"])
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format.")
    
    for key, value in update_data.items():
        setattr(record, key, value)
    
    record.estimated_phase = estimate_phase(record.cycle_start, record.cycle_length)
    db.commit()
    db.refresh(record)
    return record

@router.get("/current")
def get_current_cycle(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.query(CycleRecord).filter(
        CycleRecord.user_id == user.id
    ).order_by(CycleRecord.cycle_start.desc()).first()
    if not record:
        return {"message": "Add your cycle information to begin personal cycle tracking."}
    
    phase = estimate_phase(record.cycle_start, record.cycle_length)
    insights = get_cycle_insights(record.cycle_start, record.cycle_length)
    return {
        "record_id": record.id,
        "cycle_start": record.cycle_start.isoformat(),
        "current_phase": phase,
        "insights": insights
    }
