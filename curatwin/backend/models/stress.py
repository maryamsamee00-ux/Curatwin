from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base


class StressPrediction(Base):
    __tablename__ = "stress_predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    timestamp = Column(DateTime, server_default=func.now())
    stress_level = Column(String(20), nullable=False)
    confidence = Column(Float, default=0.0)
    model_version = Column(String(50), default="1.0.0")
    features_used = Column(String(500), default="")
    created_at = Column(DateTime, server_default=func.now())
