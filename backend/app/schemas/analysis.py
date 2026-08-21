from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VendorScoreBase(BaseModel):
    quotation_id: int
    vendor_id: int
    rfq_id: int
    price_score: Optional[float] = None
    delivery_score: Optional[float] = None
    quality_score: Optional[float] = None
    warranty_score: Optional[float] = None
    payment_score: Optional[float] = None
    reliability_score: Optional[float] = None
    final_score: Optional[float] = None
    tco: Optional[float] = None
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    recommendation_rank: Optional[int] = None
    delivery_days: Optional[int] = None
    payment_terms: Optional[str] = None


class VendorScoreResponse(VendorScoreBase):
    id: int
    vendor_name: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AnalysisResponse(BaseModel):
    rfq_id: int
    scores: list[VendorScoreResponse]
    recommendation: Optional[str] = None
