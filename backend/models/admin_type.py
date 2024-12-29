# backend/models/admin_type.py
from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AdminType(Base):
    __tablename__ = 'admin_type'

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_type_name = Column(String(50), nullable=False)
    permissions = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __init__(self, admin_type_name, permissions):
        self.admin_type_name = admin_type_name
        self.permissions = permissions

    def __repr__(self):
        return f"<AdminType(admin_type_name='{self.admin_type_name}')>"