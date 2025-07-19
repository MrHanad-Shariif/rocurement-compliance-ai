from sqlalchemy import Column, Integer, String
from app.db import Base

class ApprovedItem(Base):
    __tablename__ = "approved_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False) 