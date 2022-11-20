from typing import Final
from unittest.mock import patch

import librosa
import numpy as np
import pytest
from PIL import Image
from utilities.audio_processor import app

MODULE_PATH: Final = "utilities.audio_processor.app"


@pytest.fixture(params=range(5, 9))
def desired_duration(request):
    return request.param


@pytest.fixture
def load_librosa_mel_spectrogram(sample_wav_path, desired_duration):
    signal, sr = librosa.load(sample_wav_path, sr=22050, duration=desired_duration)
    librosa_mel = librosa.feature.melspectrogram(y=signal, sr=sr, hop_length=2048)
    return librosa_mel


@pytest.fixture
def load_sliced_audio(sample_wav_path, desired_duration):
    return app.audio_slicer(sample_wav_path, desired_segments_seconds=desired_duration)


def test_audio_slicer(load_librosa_mel_spectrogram, load_sliced_audio):
    """Tests if librosa.load generated mel spectrogram matches sliced mel spectrogram"""
    spectrogram = librosa.feature.melspectrogram(y=load_sliced_audio[0], sr=22050, hop_length=2048)
    assert np.array_equiv(load_librosa_mel_spectrogram, spectrogram)
    # check shapes of rest of slices
    for item in load_sliced_audio:
        assert (
            load_librosa_mel_spectrogram.shape
            == librosa.feature.melspectrogram(y=item, sr=22050, hop_length=2048).shape
        )


def test_transform_spectrogram(load_sliced_audio):
    """Tests if min and max are [0-255]"""
    for spectrogram in load_sliced_audio:
        transformed = app.transform_spectrogram(spectrogram)
        assert np.all((transformed >= 0) & (transformed <= 255))


def test_generate_sound_images(sample_wav_path, desired_duration):
    """Tests converting sound file to multiple images"""
    librosa_options = {"desired_segments_seconds": desired_duration}
    images = app.generate_sound_images(sample_wav_path, **librosa_options)
    counter = 0
    for image in images:
        assert isinstance(image, Image.Image)
        counter += 1
    assert int(30 / desired_duration) == counter


def test_convert_sound_to_image(sample_wav_path):
    """Tests converting sound file to one image."""
    image = app.convert_sound_to_image(sample_wav_path)
    assert isinstance(image, Image.Image)
    assert image.size == (323, 128)


@patch(f"{MODULE_PATH}.audio_slicer")
def test_duration_and_segments_seconds_not_passed(patched_audio_slicer, sample_wav_path):
    librosa_options_overwritten_in_function = ("duration", "desired_segments_seconds")
    expected_value = 20

    with patch(f"{MODULE_PATH}.spectrogram_to_image"), patch(
        f"{MODULE_PATH}.log_spectrogram"
    ), patch("librosa.feature.melspectrogram"):
        app.convert_sound_to_image(sample_wav_path, duration=20, desired_segments_seconds=13)
        assert all(
            patched_audio_slicer.call_args.kwargs[key] == expected_value
            for key in librosa_options_overwritten_in_function
        )
