import librosa
import numpy as np
import pytest
from PIL import Image
from utilities.audio_processor import app


@pytest.fixture(params=range(5, 9))
def desired_duration(request):
    return request.param


@pytest.fixture
def load_librosa_mel_spectrogram(sample_wav_path, desired_duration):
    signal, sr = librosa.load(sample_wav_path, sr=22050, duration=desired_duration)
    librosa_mel = librosa.feature.melspectrogram(y=signal, sr=sr)
    return librosa_mel


@pytest.fixture
def load_spectrogram_generator(sample_wav_path, desired_duration):
    return app.spectrogram_generator(sample_wav_path, desired_segments_seconds=desired_duration)


def test_spectrogram_generator(load_librosa_mel_spectrogram, load_spectrogram_generator):
    """Tests if librosa.load generated mel spectrogram matches sliced mel spectrogram"""
    spectrogram = next(load_spectrogram_generator)
    assert np.array_equiv(load_librosa_mel_spectrogram, spectrogram)
    assert load_librosa_mel_spectrogram.shape == spectrogram.shape
    # check shapes of rest of slices
    for item in load_spectrogram_generator:
        assert load_librosa_mel_spectrogram.shape == item.shape


def test_transform_spectrogram(load_spectrogram_generator):
    """Tests if min and max are [0-255]"""
    for spectrogram in load_spectrogram_generator:
        transformed = app.transform_spectrogram(spectrogram)
        assert np.all((transformed >= 0) & (transformed <= 255))


def test_generate_sound_images(sample_wav_path, desired_duration):
    """Tests converting sound file to multiple images"""
    librosa_options = {"desired_segments_seconds": desired_duration}
    images = app.generate_sound_images(sample_wav_path, librosa_options)
    counter = 0
    for image in images:
        assert isinstance(image, Image.Image)
        counter += 1
    assert int(30 / desired_duration) == counter


def test_convert_sound_to_image(sample_wav_path):
    """Tests converting sound file to one image."""
    image = app.convert_sound_to_image(sample_wav_path)
    assert isinstance(image, Image.Image)


def test_exception(sample_wav_path):
    """Tests the correct interface is used."""
    with pytest.raises(RuntimeError):
        librosa_options = {"desired_segments_seconds": 13, "duration": 15}
        app.convert_sound_to_image(sample_wav_path, librosa_options)
