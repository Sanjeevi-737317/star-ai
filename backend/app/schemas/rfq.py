from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RFQBase(BaseModel):
    rfq_number: str
    title: str
    department: Optional[str] = None
    product: Optional[str] = None
    quantity: Optional[int] = None
    budget: Optional[float] = None
    required_delivery_date: Optional[str] = None
    payment_terms: Optional[str] = None
    additional_requirements: Optional[str] = None
    status: str = "draft"
    created_by: Optional[int] = None


class RFQCreate(RFQBase):
    pass


class RFQUpdate(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    product: Optional[str] = None
    quantity: Optional[int] = None
    budget: Optional[float] = None
    required_delivery_date: Optional[str] = None
    payment_terms: Optional[str] = None
    additional_requirements: Optional[str] = None
    status: Optional[str] = None


class RFQResponse(RFQBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
