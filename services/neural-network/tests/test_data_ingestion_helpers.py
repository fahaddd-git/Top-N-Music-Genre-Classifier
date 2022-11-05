import pytest
from neural_network.data_ingestion_helpers import _get_genre_occurrences, train_test_split
from utilities.db.connector import sqlite_session
from utilities.db.models import Spectrogram

with sqlite_session().begin() as session:
    N = session.query(Spectrogram).count()

PARAM_NAMES = "train_frac,num_train,num_test"
PARAMS = [
    (0.5, 0.5 * N, 0.5 * N),
    (0.6, 0.6 * N, 0.4 * N),
    (0.4, 0.4 * N, 0.6 * N),
    (0.75, 0.75 * N, 0.25 * N),
    (0.813, 0.82 * N, 0.18 * N),
]


@pytest.mark.parametrize(PARAM_NAMES, PARAMS)
def test_train_test_split(train_frac, num_train, num_test):
    spectrogram_data = train_test_split(train_frac)
    assert len(spectrogram_data.train_data) == num_train
    assert len(spectrogram_data.train_labels) == num_train
    assert len(spectrogram_data.test_data) == num_test
    assert len(spectrogram_data.test_labels) == num_test


@pytest.mark.parametrize(PARAM_NAMES, PARAMS)
def test_labels_are_correct(train_frac, num_train, num_test):
    spectrogram_data = train_test_split(train_fraction=train_frac)
    for id, count in _get_genre_occurrences().items():
        label = id - 1
        assert spectrogram_data.train_labels.count(label) == num_train * count / N
        assert spectrogram_data.test_labels.count(label) == num_test * count / N
