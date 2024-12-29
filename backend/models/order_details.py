# backend/models/order_details.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from models.base import Base

class OrderDetails(Base):
    __tablename__ = 'order_details'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    tax = Column(DECIMAL(10, 2), default=0.00)
    order_status = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    payment_id = Column(Integer, ForeignKey('payment_details.payment_id'))
    
    customer = relationship('Customer', backref='orders', foreign_keys=[customer_id])
    payment = relationship('PaymentDetails', foreign_keys=[payment_id], backref='orders')
    items = relationship(
        "OrderItems",
        back_populates="order_details",
        lazy='joined',
        overlaps="order_items,order"
    )
    
    def to_dict(self):
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'total': float(self.total),
            'tax': float(self.tax),
            'order_status': self.order_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'modified_at': self.modified_at.isoformat() if self.modified_at else None,
            'payment_id': self.payment_id,
            'items': [item.to_dict() for item in self.items]
        }
    

    def __repr__(self):
        return f"<OrderDetails(order_id='{self.order_id}', customer_id='{self.customer_id}')>"