from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base


class Guardian(Base):
    __tablename__ = "guardians"

    id = Column(Integer, primary_key=True, index=True)
    student_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    guardian_name = Column(String(200), nullable=False)
    guardian_contact = Column(String(320), nullable=False)
    relationship = Column(String(100), default="")
    verification_status = Column(String(50), default="pending")
    verification_code = Column(String(20), default="")
    created_at = Column(DateTime, server_default=func.now())
