import os
from functools import cache
from pathlib import Path

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from utilities.db.constants import SQLITE_DB_PATH


@cache
def sqlite_session() -> sessionmaker:
    """
    Managed sqlite session context manager. Automatically commits and closes
    session on exit.
    Usage:

        >>>  with sqlite_session().begin() as session:
        >>>     new_genre = Genre(name="classical")
        >>>     session.add(new_genre)
    """
    if sqlite_path := os.environ.get(SQLITE_DB_PATH) is None:
        sqlite_path = (Path(__file__).parent.parent.parent / "resources/data.db").absolute()
    sqlite_url = f"sqlite:///{sqlite_path}"
    engine = create_engine(sqlite_url)
    session = sessionmaker(bind=engine)
    return session
