import os
from functools import cache

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from utilities.db.constants import SQLITE_DB_PATH


@cache
def sqlite_session() -> sessionmaker:
    """Managed sqlite session context manager. Automatically commits and closes session on exit.
    Usage:

        >>>  with sqlite_session().begin() as session:
        >>>     new_genre = Genre(name="classical")
        >>>     session.add(new_genre)
    """
    sqlite_path = os.environ.get(SQLITE_DB_PATH)
    sqlite_url = f"sqlite:////{sqlite_path}"
    engine = create_engine(sqlite_url)
    session = sessionmaker(bind=engine)
    return session
