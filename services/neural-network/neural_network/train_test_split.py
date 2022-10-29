from dataclasses import dataclass
from math import ceil

from sqlalchemy import func
from utilities.db.connector import sqlite_session
from utilities.db.models import Spectrogram


@dataclass
class SpectrogramData:
    train_data: list[bytes]
    train_labels: list[int]
    test_data: list[bytes]
    test_labels: list[int]


def _get_genre_occurances() -> dict:
    with sqlite_session().begin() as session:
        genre_count = (
            session.query(Spectrogram.genre_id, func.count(True))
            .group_by(Spectrogram.genre_id)
            .all()
        )
        return dict(genre_count)


def _get_examples(genre_id: int, n: int, skip: int) -> list[bytes]:
    with sqlite_session().begin() as session:
        results = (
            session.query(Spectrogram.image_data)
            .filter(Spectrogram.genre_id == genre_id)
            .limit(n)
            .offset(skip)
            .all()
        )
    return results


def train_test_split(train_fraction=0.8) -> SpectrogramData:
    """
    Partitions the entire database into train and test fractions
    and returns the corresponding SpectrogramData.
    """
    if 1 <= train_fraction <= 0:
        raise Exception("Train fraction must be between 0 and 1")

    test_fraction = 1 - train_fraction
    genre_occurances = _get_genre_occurances()

    train_data = []
    train_labels = []
    test_data = []
    test_labels = []
    for genre_id, num_examples in genre_occurances.items():
        num_train = ceil(num_examples * train_fraction)
        num_test = ceil(num_examples * test_fraction)

        train_data_found = _get_examples(genre_id, num_train, 0)
        test_data_found = _get_examples(genre_id, num_test, num_train)

        train_data += train_data_found
        test_data += test_data_found
        train_labels += [genre_id] * len(train_data_found)
        test_labels += [genre_id] * len(test_data_found)

    return SpectrogramData(train_data, train_labels, test_data, test_labels)


if __name__ == "__main__":
    print(len(_get_examples(1, 12, 90)))
    print(_get_genre_occurances())
    data = train_test_split(train_fraction=0.78)
    print(len(data.train_data))
    print(len(data.train_labels))
    print(len(data.test_data))
    print(len(data.test_labels))
    print(data.train_labels)
    print(data.test_labels)
