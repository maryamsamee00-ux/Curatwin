from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class GuardianCreate(BaseModel):
    guardian_name: str
    guardian_contact: str
    relationship: str = ""


class GuardianVerify(BaseModel):
    verification_code: str


class GuardianResponse(BaseModel):
    id: int
    student_user_id: int
    guardian_name: str
    guardian_contact: str
    relationship: str
    verification_status: str
    verification_code: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
