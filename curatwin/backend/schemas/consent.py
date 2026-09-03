from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ConsentCreate(BaseModel):
    guardian_id: int
    permission_type: str
    enabled: int = 0


class ConsentUpdate(BaseModel):
    enabled: int


class ConsentResponse(BaseModel):
    id: int
    user_id: int
    guardian_id: int
    permission_type: str
    enabled: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
