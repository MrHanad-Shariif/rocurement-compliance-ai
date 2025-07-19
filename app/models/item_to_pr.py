from sqlalchemy import Column, Integer, ForeignKey
from app.db import Base

class ItemToPR(Base):
    __tablename__ = "item_to_pr"
    id = Column(Integer, primary_key=True, index=True)
    pr_id = Column(Integer, ForeignKey('validations.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('approved_items.id'), nullable=False)

    def __repr__(self):
        return f"<ItemToPR(id={self.id}, pr_id={self.pr_id}, item_id={self.item_id})>" 