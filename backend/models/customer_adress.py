# backend/models/customer_address.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.customer import Customer
from sqlalchemy.ext.declarative import declarative_base
from models.base import Base

class CustomerAddress(Base):
    __tablename__ = 'customer_address'
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100), nullable=False)
    postal_code = Column(String(10), nullable=False)
    country = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=False)

    customer = relationship('Customer', backref='addresses')

    def __repr__(self):
        return f"<CustomerAddress(address_id='{self.address_id}', customer_id='{self.customer_id}')>"

    def to_dict(self):
        return {
            "address_id": self.address_id,
            "customer_id": self.customer_id,
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "city": self.city,
            "postal_code": self.postal_code,
            "country": self.country,
            "phone_number": self.phone_number
        }