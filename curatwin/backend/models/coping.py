from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from ..database import Base


class CopingIntervention(Base):
    __tablename__ = "coping_interventions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    intervention_type = Column(String(100), nullable=False)
    category = Column(String(100), default="general")
    title = Column(String(300), default="")
    recommendation = Column(Text, nullable=False)
    trigger = Column(String(200), default="")
    completed = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
