# backend/models/cart_item.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class CartItem(Base):
    __tablename__ = 'cart_item'

    cart_item_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('shopping_session.session_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add relationships
    product = relationship("Product", backref="cart_items", lazy="joined")
    session = relationship("ShoppingSession", backref="cart_items")

    def to_dict(self):
        return {
            'cart_item_id': self.cart_item_id,
            'session_id': self.session_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'product': self.product.to_dict() if self.product else None
        }