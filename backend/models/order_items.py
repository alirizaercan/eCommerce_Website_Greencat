# backend/models/order_items.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from models.base import Base

class OrderItems(Base):
    __tablename__ = 'order_items'

    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order_details.order_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    order = relationship('OrderDetails', backref='order_items')
    product = relationship('Product', backref='order_items')
    order_details = relationship(
        "OrderDetails",
        back_populates="items",
        overlaps="order,order_items"
    )
    
    def to_dict(self):
        return {
            'item_id': self.order_item_id,
            'order_id': self.order_id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'price': float(self.order.total) 
        }

    def __repr__(self):
        return f"<OrderItems(order_item_id='{self.order_item_id}', order_id='{self.order_id}')>"