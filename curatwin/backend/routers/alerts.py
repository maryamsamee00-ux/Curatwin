from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from ..database import get_db
from ..models.user import User
from ..models.alert import Alert
from ..models.guardian import Guardian
from ..models.consent import ConsentRecord
from ..middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.post("/emergency")
def trigger_emergency(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    guardians = db.query(Guardian).filter(
        Guardian.student_user_id == user.id,
        Guardian.verification_status == "verified"
    ).all()
    
    if not guardians:
        raise HTTPException(status_code=400, detail="No verified guardians found. Please add and verify a guardian first.")
    
    alerts_created = []
    for guardian in guardians:
        consents = db.query(ConsentRecord).filter(
            ConsentRecord.user_id == user.id,
            ConsentRecord.guardian_id == guardian.id,
            ConsentRecord.enabled == 1
        ).all()
        
        scope = json.dumps([c.permission_type for c in consents])
        
        alert = Alert(
            user_id=user.id,
            guardian_id=guardian.id,
            alert_type="emergency",
            status="triggered",
            shared_data_scope=scope,
            message=f"Emergency alert triggered for {user.name}. Guardian {guardian.guardian_name} has been notified with consent-granted information only."
        )
        db.add(alert)
        alerts_created.append({"guardian": guardian.guardian_name, "status": "triggered"})
    
    db.commit()
    return {"alerts": alerts_created, "message": "Emergency alerts sent to verified guardians based on your consent settings."}

@router.get("/history")
def get_alerts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.user_id == user.id).order_by(Alert.created_at.desc()).limit(20).all()
    return {
        "alerts": [
            {
                "id": a.id,
                "alert_type": a.alert_type,
                "status": a.status,
                "guardian_id": a.guardian_id,
                "message": a.message,
                "shared_data_scope": a.shared_data_scope,
                "created_at": a.created_at.isoformat() if a.created_at else None
            }
            for a in alerts
        ]
    }
