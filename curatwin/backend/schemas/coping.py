from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CopingResponse(BaseModel):
    id: int
    user_id: int
    intervention_type: str
    category: str
    title: str
    recommendation: str
    trigger: str
    completed: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
