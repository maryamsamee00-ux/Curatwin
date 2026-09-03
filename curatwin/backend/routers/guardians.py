from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random
import string
from ..database import get_db
from ..models.user import User
from ..models.guardian import Guardian
from ..schemas.guardian import GuardianCreate, GuardianResponse, GuardianVerify
from ..middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/guardians", tags=["guardians"])

@router.post("/", response_model=GuardianResponse)
def add_guardian(data: GuardianCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    code = "".join(random.choices(string.digits, k=6))
    guardian = Guardian(
        student_user_id=user.id,
        guardian_name=data.guardian_name,
        guardian_contact=data.guardian_contact,
        relationship=data.relationship,
        verification_code=code
    )
    db.add(guardian)
    db.commit()
    db.refresh(guardian)
    return guardian

@router.get("/", response_model=List[GuardianResponse])
def list_guardians(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Guardian).filter(Guardian.student_user_id == user.id).all()

@router.post("/{guardian_id}/verify", response_model=GuardianResponse)
def verify_guardian(guardian_id: int, data: GuardianVerify, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    guardian = db.query(Guardian).filter(
        Guardian.id == guardian_id, Guardian.student_user_id == user.id
    ).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian not found.")
    if guardian.verification_code != data.verification_code:
        raise HTTPException(status_code=400, detail="Invalid verification code.")
    guardian.verification_status = "verified"
    db.commit()
    db.refresh(guardian)
    return guardian

@router.delete("/{guardian_id}")
def delete_guardian(guardian_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    guardian = db.query(Guardian).filter(
        Guardian.id == guardian_id, Guardian.student_user_id == user.id
    ).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian not found.")
    db.delete(guardian)
    db.commit()
    return {"message": "Guardian removed."}
