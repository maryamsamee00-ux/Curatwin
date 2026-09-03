from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from ..database import Base


class MoodCheckin(Base):
    __tablename__ = "mood_checkins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    mood = Column(Float, default=0.0)
    perceived_stress = Column(Float, default=0.0)
    sleep_quality = Column(Float, default=0.0)
    energy_level = Column(Float, default=0.0)
    symptoms = Column(Text, default="")
    menstrual_symptoms = Column(Text, default="")
    notes = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
