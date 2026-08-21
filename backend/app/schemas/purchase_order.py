from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class PurchaseOrderBase(BaseModel):
    po_number: str
    rfq_id: int
    vendor_id: int
    quotation_id: Optional[int] = None
    items: Optional[List[Dict[str, Any]]] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total_amount: Optional[float] = None
    delivery_days: Optional[int] = None
    payment_terms: Optional[str] = None
    status: str = "draft"


class PurchaseOrderCreate(PurchaseOrderBase):
    pass


class PurchaseOrderApprove(BaseModel):
    approved_by: int


class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
