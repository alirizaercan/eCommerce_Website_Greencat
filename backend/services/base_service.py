from utils.database import Database

class BaseService:
    def __init__(self, session=None):
        self.db = Database()
        self._session = session if session else self.db.get_session()

    def _get_session(self):
        return self._session