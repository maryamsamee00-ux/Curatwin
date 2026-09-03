from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.consent import ConsentRecord
from ..models.guardian import Guardian
from ..schemas.consent import ConsentCreate, ConsentUpdate, ConsentResponse
from ..middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/consent", tags=["consent"])

@router.post("/", response_model=ConsentResponse)
def create_consent(data: ConsentCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    guardian = db.query(Guardian).filter(
        Guardian.id == data.guardian_id, Guardian.student_user_id == user.id
    ).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian not found.")
    if guardian.verification_status != "verified":
        raise HTTPException(status_code=400, detail="Guardian must be verified before granting consent.")
    
    existing = db.query(ConsentRecord).filter(
        ConsentRecord.user_id == user.id,
        ConsentRecord.guardian_id == data.guardian_id,
        ConsentRecord.permission_type == data.permission_type
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Consent for this permission already exists. Update it instead.")
    
    record = ConsentRecord(
        user_id=user.id,
        guardian_id=data.guardian_id,
        permission_type=data.permission_type,
        enabled=data.enabled
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[ConsentResponse])
def list_consents(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(ConsentRecord).filter(ConsentRecord.user_id == user.id).all()

@router.put("/{consent_id}", response_model=ConsentResponse)
def update_consent(consent_id: int, data: ConsentUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.query(ConsentRecord).filter(
        ConsentRecord.id == consent_id, ConsentRecord.user_id == user.id
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Consent record not found.")
    record.enabled = data.enabled
    db.commit()
    db.refresh(record)
    return record

@router.delete("/{consent_id}")
def revoke_consent(consent_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.query(ConsentRecord).filter(
        ConsentRecord.id == consent_id, ConsentRecord.user_id == user.id
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Consent record not found.")
    db.delete(record)
    db.commit()
    return {"message": "Consent revoked successfully."}
