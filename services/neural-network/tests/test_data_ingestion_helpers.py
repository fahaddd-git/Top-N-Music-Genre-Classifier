from functools import cache

import pytest
from neural_network.data_ingestion_helpers import _get_genre_occurrences, train_test_split
from utilities.db.connector import sqlite_session
from utilities.db.models import Spectrogram


@cache
def get_count():
    with sqlite_session().begin() as session:
        count = session.query(Spectrogram).count()
        return count


@pytest.mark.parametrize(
    "train_frac, train_expect, test_expect",
    [
        (0.5, 0.5, 0.5),
        (0.6, 0.6, 0.4),
        (0.4, 0.4, 0.6),
        (0.75, 0.75, 0.25),
        (0.813, 0.82, 0.18),
    ],
)
def test_train_test_split(train_frac, train_expect, test_expect):
    count = get_count()
    spectrogram_data = train_test_split(train_frac)
    assert len(spectrogram_data.train_data) == train_expect * count
    assert len(spectrogram_data.train_labels) == train_expect * count
    assert len(spectrogram_data.test_data) == test_expect * count
    assert len(spectrogram_data.test_labels) == test_expect * count


@pytest.mark.parametrize(
    "train_frac, train_expect, test_expect",
    [
        (0.5, 0.5, 0.5),
        (0.6, 0.6, 0.4),
        (0.4, 0.4, 0.6),
        (0.75, 0.75, 0.25),
        (0.813, 0.82, 0.18),
    ],
)
def test_labels_are_correct(train_frac, train_expect, test_expect):
    spec_data = train_test_split(train_fraction=train_frac)
    for id, count in _get_genre_occurrences().items():
        label = id - 1
        assert spec_data.train_labels.count(label) == train_expect * count
        assert spec_data.test_labels.count(label) == test_expect * count
