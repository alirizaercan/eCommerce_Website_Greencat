# backend/utils/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.customer import Base
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        self.engine = None
        self.Session = None
        self.connect()

    def connect(self):
        if self.engine is None:
            database_url = os.getenv('DATABASE_URL')
            if not database_url:
                raise ValueError("DATABASE_URL not found in environment variables")
            
            self.engine = create_engine(database_url)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        if not self.Session:
            self.connect()
        return self.Session()

    def close(self, session):
        if session:
            session.close()