# backend/models/product_image.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from models.base import Base

class ProductImage(Base):
    __tablename__ = 'product_image'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False)
    image_url = Column(String(255), nullable=False)

    # Fix relationship with optimized loading
    product = relationship(
        "Product", 
        back_populates="images", 
        lazy='joined'
    )

    def as_dict(self):
        return {
            'image_id': self.image_id,
            'product_id': self.product_id,
            'image_url': self.image_url,
        }