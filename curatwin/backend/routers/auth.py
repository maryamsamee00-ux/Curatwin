from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.profile import StudentProfile
from ..schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from ..middleware.auth_middleware import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    if len(data.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters.")
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")
    
    user = User(name=data.name, email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.flush()
    
    profile = StudentProfile(user_id=user.id, age_range=data.age_range)
    db.add(profile)
    db.commit()
    db.refresh(user)
    
    token = create_access_token({"sub": user.id})
    return TokenResponse(access_token=token, user={"id": user.id, "name": user.name, "email": user.email})

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    token = create_access_token({"sub": user.id})
    return TokenResponse(access_token=token, user={"id": user.id, "name": user.name, "email": user.email})

@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {"id": user.id, "name": user.name, "email": user.email}

@router.post("/logout")
def logout(user: User = Depends(get_current_user)):
    return {"message": "Logged out successfully."}
