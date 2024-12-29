# backend/models/shopping_session.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, text
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ShoppingSession(Base):
    __tablename__ = 'shopping_session'

    session_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id', ondelete='CASCADE'), nullable=False)
    total = Column(DECIMAL(10, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship(
        "Customer", 
        back_populates="shopping_sessions",
        lazy='joined'
    )


    @classmethod
    def restart_sequence(cls, db_session):
        """Reset sequence to continue from max id"""
        try:
            result = db_session.execute(
                text("SELECT setval('shopping_session_session_id_seq', (SELECT COALESCE(MAX(session_id), 0) FROM shopping_session))")
            ).scalar()
            db_session.commit()
            logger.info(f"Sequence reset to {result}")
            return True
        except Exception as e:
            logger.error(f"Failed to reset sequence: {e}")
            db_session.rollback()
            return False

    def as_dict(self):
        return {
            'session_id': self.session_id,
            'customer_id': self.customer_id,
            'total': float(self.total),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'modified_at': self.modified_at.isoformat() if self.modified_at else None
        }