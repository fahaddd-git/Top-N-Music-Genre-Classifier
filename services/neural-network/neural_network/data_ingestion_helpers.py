from dataclasses import dataclass
from math import ceil
from typing import Annotated

import tensorflow as tf
from numpy.typing import NDArray
from sqlalchemy import func
from tensorflow import RaggedTensor, Tensor
from utilities.db.connector import sqlite_session
from utilities.db.models import Genre, Spectrogram

# type aliases
SpectrogramDataType = Annotated[list[NDArray], "List of 2D NDArrays representing images"]
SpectrogramLabelType = Annotated[list[int], "List of integer labels"]
LabelMappingType = Annotated[dict[int, str], "Mapping of integer labels to descriptions"]


@dataclass(frozen=True, eq=False)
class SpectrogramData:
    train_data: SpectrogramDataType
    train_labels: SpectrogramLabelType
    test_data: SpectrogramDataType
    test_labels: SpectrogramLabelType
    label_mapping: LabelMappingType

    @property
    def number_of_labels(self) -> int:
        """Total number of unique labels in the dataset"""
        return len(self.label_mapping)

    @property
    def train_dataset(self) -> tuple[RaggedTensor, Tensor]:
        """Training data as a tuple comprising a ragged tensor and corresponding label tensor"""
        return tf.ragged.constant(self.train_data), tf.constant(self.train_labels)

    @property
    def test_dataset(self) -> tuple[RaggedTensor, Tensor]:
        """Testing data as a tuple comprising a ragged tensor and corresponding label tensor"""
        return tf.ragged.constant(self.test_data), tf.constant(self.test_labels)


def _get_genre_labels() -> dict[int, str]:
    """Return a genre_id -> name mapping"""
    with sqlite_session().begin() as session:
        genres = session.query(Genre).all()
        return {g.id: g.name for g in genres}


def _get_genre_occurrences() -> dict[int, int]:
    """Return a frequency map of Spectrogram genre_id -> count pairs"""
    with sqlite_session().begin() as session:
        genre_count = (
            session.query(Spectrogram.genre_id, func.count(True))
            .group_by(Spectrogram.genre_id)
            .all()
        )
        return dict(genre_count)


def _get_spectrogram_images(genre_id: int, limit: int, skip: int):
    """Return a list of spectrogram images matching the passed filters"""
    with sqlite_session().begin() as session:
        results = (
            session.query(Spectrogram)
            .filter(Spectrogram.genre_id == genre_id)
            .limit(limit)
            .offset(skip)
            .all()
        )
        spectrogram_images = [spectrogram.image_data for spectrogram in results]
        spectrogram_images = [tf.io.decode_image(x) for x in spectrogram_images]
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

        train_data_found = _get_spectrogram_images(genre_id, num_train, 0)
        test_data_found = _get_spectrogram_images(genre_id, num_test, num_train)

        train_data += train_data_found
        test_data += test_data_found
        train_labels += [genre_id] * len(train_data_found)
        test_labels += [genre_id] * len(test_data_found)

    genre_labels = _get_genre_labels()
    return SpectrogramData(train_data, train_labels, test_data, test_labels, genre_labels)
