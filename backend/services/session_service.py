# backend/services/session_service.py
from sqlalchemy.orm import Session
from models.shopping_session import ShoppingSession
from utils.database import Database
import logging

logger = logging.getLogger(__name__)

class SessionService:
    def __init__(self, db_session: Session = None):
        if db_session is None:
            db = Database()
            self.db = db.get_session()
        else:
            self.db = db_session

    def create_session(self, customer_id, total=0):
        try:
            new_session = ShoppingSession(customer_id=customer_id, total=total)
            self.db.add(new_session)
            self.db.commit()
            self.db.refresh(new_session)
            return new_session
        except Exception as e:
            logger.error(f"Failed to create session: {str(e)}")
            self.db.rollback()
            raise ValueError(f"Failed to create shopping session: {str(e)}")

    def get_session(self, session_id):
        try:
            session = self.db.query(ShoppingSession).filter_by(session_id=session_id).first()
            return session.as_dict() if session else None
        except Exception as e:
            logger.error(f"Error getting session: {str(e)}")
            return None

    def update_session(self, session_id, total):
        try:
            session = self.db.query(ShoppingSession).filter_by(session_id=session_id).first()
            if session:
                session.total = total
                self.db.commit()
                self.db.refresh(session)
                return session.as_dict()
            return None
        except Exception as e:
            logger.error(f"Error updating session: {str(e)}")
            self.db.rollback()
            return None

    def delete_session(self, session_id):
        try:
            session = self.db.query(ShoppingSession).filter_by(session_id=session_id).first()
            if session:
                self.db.delete(session)
                self.db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting session: {str(e)}")
            self.db.rollback()
            return False