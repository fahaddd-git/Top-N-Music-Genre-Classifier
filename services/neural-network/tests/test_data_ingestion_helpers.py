from typing import Final
from unittest.mock import patch

import pytest
from neural_network.data_ingestion_helpers import _get_genre_occurrences, train_test_split

MODULE_PATH: Final = "neural_network.data_ingestion_helpers"


@pytest.fixture(scope="function", autouse=True)
def patch_session(patched_session):
    with patch(f"{MODULE_PATH}.sqlite_session", return_value=patched_session):
        yield


@pytest.mark.parametrize(
    "train_frac, num_train, num_test",
    [
        (0.500, 0.50, 0.50),
        (0.600, 0.60, 0.40),
        (0.400, 0.40, 0.60),
        (0.750, 0.75, 0.25),
        (0.813, 0.82, 0.18),
    ],
)
@patch(f"{MODULE_PATH}.tf.io.decode_image")
def test_train_test_split(patched_tf_io_decode, train_frac, num_train, num_test, num_spectrograms):
    patched_tf_io_decode.return_value = None
    spectrogram_data = train_test_split(train_frac)
    assert len(spectrogram_data.train_data) == num_train * num_spectrograms
    assert len(spectrogram_data.train_labels) == num_train * num_spectrograms
    assert len(spectrogram_data.test_data) == num_test * num_spectrograms
    assert len(spectrogram_data.test_labels) == num_test * num_spectrograms


@pytest.mark.parametrize(
    "train_frac, num_train, num_test",
    [
        (0.500, 0.50, 0.50),
        (0.600, 0.60, 0.40),
        (0.400, 0.40, 0.60),
        (0.750, 0.75, 0.25),
        (0.813, 0.82, 0.18),
    ],
)
@patch(f"{MODULE_PATH}.tf.io.decode_image")
def test_labels_are_correct(
    patched_tf_io_decode, train_frac, num_train, num_test, num_spectrograms
):
    patched_tf_io_decode.return_value = None
    spectrogram_data = train_test_split(train_frac)
    for id, count in _get_genre_occurrences().items():
        label = id - 1
        assert spectrogram_data.train_labels.count(label) == num_train * count
        assert spectrogram_data.test_labels.count(label) == num_test * count
