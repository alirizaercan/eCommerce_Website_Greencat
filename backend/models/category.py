# models/category.py
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description