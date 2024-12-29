# backend/models/carrier.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from models.base import Base

class Carrier(Base):
    __tablename__ = 'carrier'

    carrier_id = Column(Integer, primary_key=True, autoincrement=True)
    carrier_name = Column(String(255), nullable=False)
    carrier_phone = Column(String(15), nullable=False)
    carrier_email = Column(String(255), unique=True, nullable=False)
    
    def __init__(self, carrier_name, carrier_phone, carrier_email):
        self.carrier_name = carrier_name
        self.carrier_phone = carrier_phone
        self.carrier_email = carrier_email

    def __repr__(self):
        return f"<Carrier(carrier_name='{self.carrier_name}')>"
