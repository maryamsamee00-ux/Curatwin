from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from ..database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    guardian_id = Column(Integer, ForeignKey("guardians.id"), nullable=True)
    alert_type = Column(String(100), nullable=False)
    status = Column(String(50), default="created")
    shared_data_scope = Column(Text, default="{}")
    message = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
