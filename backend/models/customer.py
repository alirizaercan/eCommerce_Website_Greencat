# backend/models/customer.py
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(75), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    login_attempts = Column(Integer, default=0)
    wrong_login_attempts = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __init__(self, first_name, last_name, username, email, password, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.phone_number = phone_number
        
    def __repr__(self):
        return f"<Customer(username='{self.username}', email='{self.email}')>"
