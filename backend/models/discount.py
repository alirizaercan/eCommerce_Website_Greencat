# backend/models/discount.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from models.base import Base

class Discount(Base):
    __tablename__ = 'discount'

    discount_id = Column(Integer, primary_key=True, autoincrement=True)
    discount_name = Column(String(50), nullable=False)
    discount_description = Column(Text)
    discount_percentage = Column(DECIMAL(5, 2), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Add relationship
    products = relationship("Product", back_populates="discount")

    def as_dict(self):
        return {
            'discount_id': self.discount_id,
            'discount_name': self.discount_name,
            'discount_description': self.discount_description,
            'discount_percentage': str(self.discount_percentage),
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'modified_at': self.modified_at.isoformat() if self.modified_at else None
        }

    def __repr__(self):
        return f"<Discount(discount_name='{self.discount_name}')>"
