from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..middleware.auth_middleware import get_current_user
from ..services.digital_twin import compute_digital_twin
from ..services.affective import estimate_affective_state

router = APIRouter(prefix="/api/digital-twin", tags=["digital-twin"])

@router.get("/state")
def get_twin_state(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    twin = compute_digital_twin(user.id, db)
    affective = estimate_affective_state(user.id, db)
    return {"digital_twin": twin, "affective_state": affective}
