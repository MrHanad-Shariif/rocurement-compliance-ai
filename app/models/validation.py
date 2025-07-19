from sqlalchemy import Column, Integer, Text, String, TIMESTAMP
from app.db import Base

class Validation(Base):
    __tablename__ = "validations"
    id = Column(Integer, primary_key=True, index=True)
    legal_entity_id = Column(Integer)
    item_type = Column(Text)
    description = Column(Text)
    quantity = Column(Integer)
    result = Column(Text)
    vendor_ids = Column(Text)
    rfq_file = Column(Text)
    created_at = Column(TIMESTAMP) 