import librosa
import numpy as np
import pytest
from PIL import Image
from utilities.audio_processor import app


@pytest.fixture
def load_librosa_mel_spectrogram(sample_wav_path):
    signal, sr = librosa.load(sample_wav_path, sr=22050, duration=30)
    librosa_mel = librosa.feature.melspectrogram(
        y=signal, sr=sr, n_fft=2048, hop_length=2048, center=False
    )
    return librosa_mel


@pytest.fixture
def load_stream_spectrogram(sample_wav_path):
    return app.stream_spectrogram(sample_wav_path)


def test_stream_spectrogram(load_librosa_mel_spectrogram, load_stream_spectrogram):
    """Tests if librosa.load generated mel spectrogram matches streamed mel spectrogram"""
    assert load_librosa_mel_spectrogram.shape == load_stream_spectrogram.shape
    assert np.array_equiv(load_librosa_mel_spectrogram, load_stream_spectrogram)


def test_transform_spectrogram(load_stream_spectrogram):
    """Tests if min and max are [0-255]"""
    assert np.all((load_stream_spectrogram >= 0) & (load_stream_spectrogram <= 255))


def test_convert_sound_to_image(sample_wav_path):
    """Tests converting log spectrogram to image"""
    result = app.convert_sound_to_image(sample_wav_path)
    assert isinstance(result, Image.Image)
