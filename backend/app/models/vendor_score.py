from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, func

from app.database import Base


class VendorScore(Base):
    __tablename__ = "vendor_scores"

    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    rfq_id = Column(Integer, ForeignKey("rfqs.id"), nullable=False)
    price_score = Column(Numeric(5, 2), nullable=True)
    delivery_score = Column(Numeric(5, 2), nullable=True)
    quality_score = Column(Numeric(5, 2), nullable=True)
    warranty_score = Column(Numeric(5, 2), nullable=True)
    payment_score = Column(Numeric(5, 2), nullable=True)
    reliability_score = Column(Numeric(5, 2), nullable=True)
    final_score = Column(Numeric(6, 2), nullable=True)
    tco = Column(Numeric(15, 2), nullable=True)
    risk_score = Column(Numeric(5, 2), nullable=True)
    risk_level = Column(String(20), nullable=True)
    recommendation_rank = Column(Integer, nullable=True)
    delivery_days = Column(Integer, nullable=True)
    payment_terms = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
