from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class QuotationItem(BaseModel):
    name: str
    quantity: int
    unit_price: float
    discount: Optional[float] = 0.0


class QuotationExtractedData(BaseModel):
    vendor_name: Optional[str] = None
    quotation_number: Optional[str] = None
    currency: Optional[str] = "INR"
    items: List[QuotationItem] = []
    subtotal: Optional[float] = 0.0
    tax: Optional[float] = 0.0
    shipping: Optional[float] = 0.0
    total: Optional[float] = 0.0
    delivery_days: Optional[int] = None
    payment_terms: Optional[str] = None
    warranty: Optional[str] = None
    risks: List[str] = []


class QuotationBase(BaseModel):
    rfq_id: int
    vendor_id: int
    file_path: Optional[str] = None
    extracted_data: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    shipping: Optional[float] = None
    total: Optional[float] = None
    delivery_days: Optional[int] = None
    payment_terms: Optional[str] = None
    warranty: Optional[str] = None
    status: str = "uploaded"


class QuotationCreate(QuotationBase):
    pass


class QuotationResponse(QuotationBase):
    id: int
    quotation_number: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
