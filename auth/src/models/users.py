from sqlalchemy import Column, Integer, Float, String, JSON
from models.base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    user_metadata = Column(JSON, nullable=True)
