from functools import cache
from unittest.mock import patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utilities.db.models import _BaseModel


@cache
def patched_session():
    engine = create_engine("sqlite://")
    # see https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData.create_all
    _BaseModel.metadata.create_all(bind=engine)  # noinspection PyProtectedMember

    # first row has column names, so skip those
    engine.execute(f".import --csv --skip 1 {'./fixtures/genres.csv'} Genres")
    engine.execute(f".import --csv --skip 1 {'./fixtures/spectrograms.csv'} Spectrograms")
    session = sessionmaker(bind=engine)
    return session


@pytest.fixture(scope="session", autouse=True)
def patch_test_database():
    # this may not actually work, but it's essentially what has to happen - the question is how
    # to patch the correct thing so that this gets patched *wherever* it's used
    with patch("utilities.db.connector.sqlite_session", return_value=patched_session):
        yield
