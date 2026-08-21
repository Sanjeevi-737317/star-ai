from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, server_default="procurement")
    is_active = Column(Integer, nullable=False, server_default="1")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
