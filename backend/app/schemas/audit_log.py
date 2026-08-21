from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AuditLogResponse(BaseModel):
    id: int
    action: str
    entity_type: str
    entity_id: Optional[int] = None
    user_id: Optional[int] = None
    details: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
