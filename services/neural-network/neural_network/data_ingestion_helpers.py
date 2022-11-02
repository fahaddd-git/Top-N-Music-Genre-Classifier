from dataclasses import dataclass
from math import ceil

import numpy as np
from numpy.typing import NDArray
from sqlalchemy import func
from utilities.db.connector import sqlite_session
from utilities.db.models import Genre, Spectrogram


@dataclass
class SpectrogramData:
    train_data: list[NDArray]
    train_labels: NDArray[int]
    test_data: list[NDArray]
    test_labels: NDArray[int]


def get_labels() -> dict:
    with sqlite_session().begin() as session:
        genres = session.query(Genre).all()
        return {g.id: g.name for g in genres}


def _get_genre_occurrences() -> dict:
    with sqlite_session().begin() as session:
        genre_count = (
            session.query(Spectrogram.genre_id, func.count(True))
            .group_by(Spectrogram.genre_id)
            .all()
        )
        return dict(genre_count)


def _get_examples(genre_id: int, n: int, skip: int) -> list[NDArray]:
    with sqlite_session().begin() as session:
        results = (
            session.query(Spectrogram)
            .filter(Spectrogram.genre_id == genre_id)
            .limit(n)
            .offset(skip)
            .all()
        )
        spectrogram_images = [np.array(spectrogram.image) for spectrogram in results]
    return spectrogram_images


def train_test_split(train_fraction: float = 0.8) -> SpectrogramData:
    """
    Partitions the entire database into train and test fractions
    and returns the corresponding SpectrogramData.
    """
    if not (0 <= train_fraction <= 1):
        raise ValueError("Train fraction must be between 0 and 1")

    test_fraction = 1.0 - train_fraction
    genre_occurrences = _get_genre_occurrences()

    train_data = []
    train_labels = []
    test_data = []
    test_labels = []
    for genre_id, num_examples in genre_occurrences.items():
        num_train = ceil(num_examples * train_fraction)
        num_test = ceil(num_examples * test_fraction)

        train_data_found = _get_examples(genre_id, num_train, 0)
        test_data_found = _get_examples(genre_id, num_test, num_train)

        train_data += train_data_found
        test_data += test_data_found
        train_labels += [genre_id] * len(train_data_found)
        test_labels += [genre_id] * len(test_data_found)

    # convert 1-indexed genre_id to 0-indexed labels
    train_labels = np.array(train_labels) - 1
    test_labels = np.array(test_labels) - 1

    return SpectrogramData(train_data, train_labels, test_data, test_labels)


# if __name__ == "__main__":
#     print(len(_get_examples(1, 12, 90)))
#     print(_get_genre_occurrences())
#     data = train_test_split(train_fraction=0.78)
#     print(len(data.train_data))
#     print(len(data.train_labels))
#     print(len(data.test_data))
#     print(len(data.test_labels))
#     print(data.train_labels)
#     print(data.test_labels)
