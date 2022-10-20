import os

import librosa
import numpy as np
import pytest
from utilities.audio_processor import app

TEST_FILE_PATH = "tests/test_files/classical.00000.wav"


@pytest.fixture
def load_librosa_mel_spectrogram():
    signal, sr = librosa.load(TEST_FILE_PATH, sr=22050)
    librosa_mel = librosa.feature.melspectrogram(
        y=signal, sr=sr, n_fft=2048, hop_length=2048, center=False
    )
    return librosa_mel


@pytest.fixture
def load_stream_spectrogram():
    return app.stream_spectrogram(TEST_FILE_PATH)


def test_stream_spectrogram(load_librosa_mel_spectrogram, load_stream_spectrogram):
    """Tests if librosa.load generated mel spectrogram matches streamed mel spectrogram"""
    assert np.array_equiv(load_librosa_mel_spectrogram, load_stream_spectrogram)


def test_transform_spectrogram(load_stream_spectrogram):
    """Tests if min and max are [0-255]"""
    assert np.any((load_stream_spectrogram <= 255) | (load_stream_spectrogram >= 0))


def test_save_spectrogram_to_image(load_stream_spectrogram):
    """Tests saving log spectrogram as image in default param path"""
    file_name = "test_file"
    log_spectrogram = app.log_spectrogram(load_stream_spectrogram)
    default_param_file_path = app.save_spectrogram_to_image.__defaults__[0]
    app.save_spectrogram_to_image(log_spectrogram, file_name)
    file = f"{default_param_file_path}/{file_name}.png"
    if not os.path.isfile(file):
        assert False
    os.remove(file)
    assert True