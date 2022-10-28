import os
from functools import cache
from pathlib import Path

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

# default location of sqlite db is ../../resources/data.db
_SQLITE_DB_ENV_VAR = "DB_PATH"
_RESOURCES_DIRECTORY_LEVELS_UP = 2
_DEFAULT_SQLITE_DATABASE_NAME = "resources/data.db"


def _get_sqlite_url() -> str:
    """Return a url to the sqlite database specified in ``_SQLITE_DB_ENV_VAR``"""
    sqlite_path = os.environ.get(_SQLITE_DB_ENV_VAR)
    try:
        sqlite_path = Path(sqlite_path).resolve(strict=True)
    except (TypeError, FileNotFoundError):
        resources_directory = Path(__file__).resolve().parents[_RESOURCES_DIRECTORY_LEVELS_UP]
        sqlite_path = resources_directory / _DEFAULT_SQLITE_DATABASE_NAME
    return f"sqlite:////{sqlite_path}"


@cache
def sqlite_session() -> sessionmaker:
    """Managed sqlite session context manager. Automatically commits and closes session on exit.
    Usage:

        >>>  with sqlite_session().begin() as session:
        >>>     new_genre = Genre(name="classical")
        >>>     session.add(new_genre)

    See also:
        https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker.begin
    """
    sqlite_url = _get_sqlite_url()
    engine = create_engine(sqlite_url)
    session = sessionmaker(bind=engine)
    return session
