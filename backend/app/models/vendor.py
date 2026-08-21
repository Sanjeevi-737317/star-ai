from sqlalchemy import Column, DateTime, Integer, Numeric, String, Text, func

from app.database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    category = Column(String(100), nullable=True)
    rating = Column(Numeric(3, 2), nullable=True)
    reliability_score = Column(Numeric(5, 2), nullable=True)
    avg_delivery_days = Column(Integer, nullable=True)
    total_orders = Column(Integer, nullable=True, server_default="0")
    address = Column(Text, nullable=True)
    gst_number = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
