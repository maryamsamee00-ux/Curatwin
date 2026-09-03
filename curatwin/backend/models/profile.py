from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    age_range = Column(String(20), default="18-24")
    university = Column(String(300), default="")
    baseline_stress = Column(Float, default=0.0)
    baseline_mood = Column(Float, default=0.0)
    baseline_sleep = Column(Float, default=0.0)
    onboarding_complete = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
