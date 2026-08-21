from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InventoryBase(BaseModel):
    po_id: int
    product_name: str
    quantity: int
    expected_delivery_date: Optional[str] = None
    status: str = "pending"


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    product_name: Optional[str] = None
    quantity: Optional[int] = None
    expected_delivery_date: Optional[str] = None
    status: Optional[str] = None


class InventoryResponse(InventoryBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
