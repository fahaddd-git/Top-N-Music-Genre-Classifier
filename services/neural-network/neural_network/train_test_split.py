import numpy as np
from utilities.db.connector import sqlite_session
from utilities.db.models import Spectrogram, Genre
from sqlalchemy import select


def _get_genre_occurances() -> dict:
    occurances = {}
    with sqlite_session().begin() as session:
        genres = session.query(Genre).all()
        for genre in genres:
            occurances[genre.name] = 0

        for genres in genres:
            genre_count = session.execute(select(Spectrogram).filter_by(genre_id=genre.id)).count()

            occurances[genres.name] = genre_count

        return occurances

# def train_test_split(train_fraction=0.8) -> (np.ndarray, np.ndarray):
#     if 1 <= train_fraction <= 0:
#         raise Exception("Train fraction must be between 0 and 1")
#     test_fraction = 1 - train_fraction
#


if __name__ == "__main__":
    print(_get_genre_occurances())
