import os

import pytest
from utilities.db.connector import sqlite_session
from utilities.db.constants import SQLITE_DB_PATH


@pytest.fixture(scope="function")
def with_unset_db_path():
    sqlite_db_path = os.environ.pop(SQLITE_DB_PATH, None)
    yield
    if sqlite_db_path is not None:
        os.environ[SQLITE_DB_PATH] = sqlite_db_path


@pytest.fixture(scope="function")
def with_invalid_db_path():
    sqlite_db_path = os.environ.pop(SQLITE_DB_PATH, None)

    os.environ[SQLITE_DB_PATH] = "/this/path/does/not/exist.db"
    yield
    if sqlite_db_path is not None:
        os.environ[SQLITE_DB_PATH] = sqlite_db_path


def test_sqlite_session_raises_runtime_error(with_unset_db_path):
    with pytest.raises(RuntimeError):
        sqlite_session()


def test_sqlite_session_raises_file_not_found(with_invalid_db_path):
    with pytest.raises(FileNotFoundError):
        sqlite_session()
