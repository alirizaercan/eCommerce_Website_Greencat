# backend/models/payment_details.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from models.base import Base

class PaymentDetails(Base):
    __tablename__ = 'payment_details'

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order_details.order_id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    tax = Column(DECIMAL(10, 2), default=0.00)
    provider = Column(String(50))
    status = Column(String(25), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    order_details = relationship('OrderDetails',
                               foreign_keys=[order_id],
                               backref='payment_details')

    def __repr__(self):
        return f"<PaymentDetails(payment_id='{self.payment_id}', amount='{self.amount}')>"