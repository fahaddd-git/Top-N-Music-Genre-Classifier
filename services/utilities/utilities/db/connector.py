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
    try:
        sqlite_path = Path(os.environ[SQLITE_DB_PATH]).resolve(strict=True)
    except KeyError:
        raise RuntimeError(f"'{SQLITE_DB_PATH}' environment variable not set")
    except (FileNotFoundError, RuntimeError):
        raise FileNotFoundError(f"Path '{os.environ.get(SQLITE_DB_PATH, '')}' does not exist")
    sqlite_url = f"sqlite:///{sqlite_path}"
    engine = create_engine(sqlite_url)
    session = sessionmaker(bind=engine)
    return session
