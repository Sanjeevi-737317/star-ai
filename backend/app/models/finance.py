from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, func

from app.database import Base


class Finance(Base):
    __tablename__ = "finance"

    id = Column(Integer, primary_key=True, index=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    due_date = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False, server_default="draft")
    payment_terms = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
