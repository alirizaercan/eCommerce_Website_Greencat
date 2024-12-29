# backend/models/product.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, Float, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.base import Base

class Product(Base):
    __tablename__ = 'product'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(100), nullable=False)
    product_description = Column(Text)
    sku = Column(String(100), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category.category_id', ondelete='SET NULL'))
    inventory_id = Column(Integer, ForeignKey('inventory.inventory_id', ondelete='SET NULL'))
    price = Column(DECIMAL(10, 2), nullable=False)
    tax = Column(DECIMAL(10, 2), default=0.00)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    discount_id = Column(Integer, ForeignKey('discount.discount_id', ondelete='SET NULL'))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    category = relationship('Category', back_populates='products', lazy='joined')
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    inventory = relationship('Inventory', back_populates='products')
    discount = relationship('Discount', back_populates='products')

    def as_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_description': self.product_description,
            'sku': self.sku,
            'category_id': self.category_id,
            'category': self.category.as_dict() if self.category else None,
            'inventory': self.inventory.as_dict() if self.inventory else None,
            'price': str(self.price),
            'tax': str(self.tax),
            'rating': self.rating,
            'review_count': self.review_count,
            'discount': self.discount.as_dict() if self.discount else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'modified_at': self.modified_at.isoformat() if self.modified_at else None,
        }

    def __repr__(self):
        return f"<Product(product_id={self.product_id}, product_name={self.product_name})>"
