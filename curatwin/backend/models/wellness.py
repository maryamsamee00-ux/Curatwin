from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from ..database import Base


class WellnessData(Base):
    __tablename__ = "wellness_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    timestamp = Column(DateTime, server_default=func.now())
    ppg_hrv = Column(Float, default=0.0)
    gsr_amplitude = Column(Float, default=0.0)
    skin_temp = Column(Float, default=36.5)
    imu_activity = Column(Float, default=0.0)
    heart_rate = Column(Float, default=0.0)
    source = Column(String(50), default="simulator")
    raw_json = Column(Text, default="{}")
    created_at = Column(DateTime, server_default=func.now())
