from utilities.db.connector import sqlite_session


class DatabaseManager:
    def __init__(self):
        self.session = sqlite_session().begin()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        self.session.close_all()
