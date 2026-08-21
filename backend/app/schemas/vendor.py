from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VendorBase(BaseModel):
    vendor_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    reliability_score: Optional[float] = None
    avg_delivery_days: Optional[int] = None
    total_orders: Optional[int] = 0
    address: Optional[str] = None
    gst_number: Optional[str] = None


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    reliability_score: Optional[float] = None
    avg_delivery_days: Optional[int] = None
    total_orders: Optional[int] = None
    address: Optional[str] = None
    gst_number: Optional[str] = None


class VendorResponse(VendorBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class VendorEvaluateRequest(BaseModel):
    vendor_id: int
    name: str
    rating: Optional[float] = None
    reliability_score: Optional[float] = None
    avg_delivery_days: Optional[int] = None
    total_orders: Optional[int] = None
    category: Optional[str] = None


class VendorEvaluateResponse(BaseModel):
    overall_score: int
    price_score: int
    delivery_score: int
    reliability_score: int
    terms_score: int
    risk: str
    recommendation: str
