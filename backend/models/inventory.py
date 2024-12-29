# backend/models/inventory.py
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import relationship
from models.base import Base

class Inventory(Base):
    __tablename__ = 'inventory'

    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Add relationship
    products = relationship("Product", back_populates="inventory")

    def as_dict(self):
        return {
            'inventory_id': self.inventory_id,
            'quantity': self.quantity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'modified_at': self.modified_at.isoformat() if self.modified_at else None
        }

    def __repr__(self):
        return f"<Inventory(quantity={self.quantity})>"