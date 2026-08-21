from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func

from app.database import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String(100), unique=True, nullable=False)
    rfq_id = Column(Integer, ForeignKey("rfqs.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=True)
    items = Column(Text, nullable=True)
    subtotal = Column(Numeric(15, 2), nullable=True)
    tax = Column(Numeric(15, 2), nullable=True)
    total_amount = Column(Numeric(15, 2), nullable=True)
    delivery_days = Column(Integer, nullable=True)
    payment_terms = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, server_default="draft")
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
