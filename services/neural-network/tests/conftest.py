import csv
from datetime import datetime
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utilities.db.models import Genre, Spectrogram, _BaseModel


@pytest.fixture(scope="session", autouse=True)
def patched_session():
    """Patched sessionmaker to in-memory database"""
    engine = create_engine("sqlite://")
    # see https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData.create_all
    _BaseModel.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)

    # effectively engine.execute(".import --csv --skip 1 ./fixtures/genres.csv Genres")
    # except that the dot-directives aren't SQL statements and require using the sqlite3 binary
    genres_csv_path = Path(__file__).resolve().parent / "fixtures/genres.csv"
    with session.begin() as current_session, open(genres_csv_path) as genres:
        genre_rows = csv.DictReader(genres)
        objects = (Genre(**row) for row in genre_rows)
        current_session.add_all(objects)

    # engine.execute(".import --csv --skip 1 ./fixtures/spectrograms.csv Spectrograms")
    spectrograms_csv_path = Path(__file__).resolve().parent / "fixtures/spectrograms.csv"
    with session.begin() as current_session, open(spectrograms_csv_path) as spectrograms:
        spectrogram_rows = csv.DictReader(spectrograms)
        overwrite_args = {"image_data": b"", "last_modified": datetime.now()}
        objects = (Spectrogram(**{**row, **overwrite_args}) for row in spectrogram_rows)
        current_session.add_all(objects)

    return session


@pytest.fixture(scope="session")
def num_spectrograms(patched_session):
    with patched_session.begin() as session:
        return session.query(Spectrogram).count()
