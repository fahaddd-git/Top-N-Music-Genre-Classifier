from os import PathLike
from typing import Iterator, TypeAlias

import librosa
import numpy as np
from numpy.typing import NDArray
from PIL import Image

PILImage: TypeAlias = Image.Image


def spectrogram_generator(
    file_path: str | PathLike,
    desired_segments_seconds: int = 5,
    sample_rate: int = 22050,
    duration: int = 90,
) -> Iterator[NDArray]:
    """Converts an audio stream to a mel spectrogram.

    :param file_path: Path to audio file
    :param desired_segments_seconds: Seconds of audio to slice when creating the mel spectrogram.
        Equal segments of this param value are made as the duration of the audio file allows.
    :param sample_rate: Sample rate to down sample audio to, in Hz
    :param duration: How long of audio file to load. Less is loaded if clip length < duration
    :return: Power Mel Spectrogram constructed from audio file with n_mels=128
    """
    audio_data, sr = librosa.load(file_path, sr=sample_rate, mono=True, duration=duration)
    clip_duration = librosa.get_duration(y=audio_data, sr=sr)
    # available slices of desired_segments_seconds
    possible_segments = int(clip_duration / desired_segments_seconds)

    # Logic to convert STFTs to mel spectrogram inspired by:
    # URL:  https://librosa.org/doc/main/generated/librosa.feature.melspectrogram.html
    # Date: 11/12/2022
    total_sample_length = sample_rate * possible_segments
    samples_per_segment = int((total_sample_length / possible_segments) * desired_segments_seconds)
    for segment_number in range(possible_segments):
        start = samples_per_segment * segment_number
        end = start + samples_per_segment
        mel_spectro = librosa.feature.melspectrogram(
            y=audio_data[start:end],
            sr=sample_rate,
            n_mels=128,
        )
        yield mel_spectro


def transform_spectrogram(spectrogram: NDArray) -> NDArray:
    """Applies standardization and contrast normalization to spectrogram.
    This is so that the spectrogram, a numpy array, can be cast as a greyscale image.

    :param spectrogram: Spectrogram to be transformed
    :return: Standardized and Contrast Normalized spectrogram.  All values between [0-255]
    """
    # standardize data https://en.wikipedia.org/wiki/Standard_score
    standardized = (spectrogram - spectrogram.mean()) / spectrogram.std()
    standardized_min = standardized.min()
    # contrast normalization for greyscale image
    # Adapted from:
    # https://stackoverflow.com/questions/70783357/how-do-i-normalize-the-pixel-value-of-an-image-to-01
    # Date: 10/22/2022
    spec_scaled = (standardized - standardized_min) / (standardized.max() - standardized_min) * 255
    return spec_scaled.astype(np.uint8)


def spectrogram_to_image(spectrogram: NDArray) -> PILImage:
    """Spectrogram array as image in greyscale standardized and contrast normalized.

    :param spectrogram: Spectrogram to be converted to image
    :return: spectrogram as PIL Image
    """

    rescaled = transform_spectrogram(spectrogram)
    image = Image.fromarray(rescaled, mode="L")
    return image


def log_spectrogram(mel_spectrogram: NDArray) -> NDArray:
    """Log mel spectrogram from spectrogram.
    In a log mel spectrogram, amplitude is converted to decibels which follows a logarithmic scale.

    :param mel_spectrogram: Mel spectrogram to be converted
    :return: Log Mel Spectrogram
    """
    log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
    return log_mel_spectrogram


def convert_sound_to_image(
    sound_file_path: str | PathLike, duration: int = 30, **librosa_options
) -> PILImage:
    """Interface for converting sound to single image.

    Default ``librosa_options`` are:
        * sample_rate: int = 22050

    :param sound_file_path: Path to audio file
    :param duration: Length of audio file to generate spectrogram for in seconds (default 30)
    :param librosa_options: Options used by Librosa for creating the spectrogram
    :return: Log Mel Spectrogram as PIL Image instance
    """
    librosa_options = {
        **librosa_options,
        "desired_segments_seconds": duration,
        "duration": duration,
    }
    spectrogram_gen = spectrogram_generator(sound_file_path, **librosa_options)
    spec = next(spectrogram_gen)

    log_spec = log_spectrogram(spec)
    image = spectrogram_to_image(log_spec)
    return image


def generate_sound_images(sound_file_path: str | PathLike, **librosa_options) -> Iterator[PILImage]:
    """Interface for converting sound to multiple images

    Default ``librosa_options`` are:
        * desired_segments_seconds: int = 5
        * sample_rate: int = 22050
        * duration: int = 30

    :param sound_file_path: Path to audio file
    :param librosa_options: Options used by Librosa for creating the spectrogram
    :return: Generator of Log Mel Spectrograms as PIL Image instances
    """
    spectrogram_gen = spectrogram_generator(sound_file_path, **librosa_options)
    for spec in spectrogram_gen:
        log_spec = log_spectrogram(spec)
        image = spectrogram_to_image(log_spec)
        yield image
