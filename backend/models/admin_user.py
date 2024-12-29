# backend/models/admin_user.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from .admin_type import AdminType, Base

class AdminUser(Base):
    __tablename__ = 'admin_user'

    admin_user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    type_id = Column(Integer, ForeignKey('admin_type.admin_id'), nullable=False)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    admin_type = relationship("AdminType", backref="admin_users", foreign_keys=[type_id])

    def __init__(self, username, password, first_name, last_name, type_id):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.type_id = type_id

    def __repr__(self):
        return f"<AdminUser(username='{self.username}')>"