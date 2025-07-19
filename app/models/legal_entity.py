from sqlalchemy import Column, Integer, String
from app.db import Base

class LegalEntity(Base):
    __tablename__ = "legal_entities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False) 