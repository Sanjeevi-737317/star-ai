from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.sql import expression

from app.database import Base


class RFQ(Base):
    __tablename__ = "rfqs"

    id = Column(Integer, primary_key=True, index=True)
    rfq_number = Column(String(100), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    department = Column(String(100), nullable=True)
    product = Column(String(255), nullable=True)
    quantity = Column(Integer, nullable=True)
    budget = Column(Numeric(15, 2), nullable=True)
    required_delivery_date = Column(String(50), nullable=True)
    payment_terms = Column(String(255), nullable=True)
    additional_requirements = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, server_default="draft")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
