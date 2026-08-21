from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FinanceBase(BaseModel):
    po_id: int
    vendor_id: int
    amount: float
    due_date: Optional[str] = None
    status: str = "draft"
    payment_terms: Optional[str] = None


class FinanceCreate(FinanceBase):
    pass


class FinanceUpdate(BaseModel):
    amount: Optional[float] = None
    due_date: Optional[str] = None
    status: Optional[str] = None
    payment_terms: Optional[str] = None


class FinanceResponse(FinanceBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
