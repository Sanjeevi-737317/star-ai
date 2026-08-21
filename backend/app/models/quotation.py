from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func

from app.database import Base


class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, index=True)
    quotation_number = Column(String(100), unique=True, nullable=False)
    rfq_id = Column(Integer, ForeignKey("rfqs.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    file_path = Column(String(500), nullable=True)
    extracted_data = Column(Text, nullable=True)
    subtotal = Column(Numeric(15, 2), nullable=True)
    tax = Column(Numeric(15, 2), nullable=True)
    shipping = Column(Numeric(15, 2), nullable=True)
    total = Column(Numeric(15, 2), nullable=True)
    delivery_days = Column(Integer, nullable=True)
    payment_terms = Column(String(255), nullable=True)
    warranty = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, server_default="uploaded")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
