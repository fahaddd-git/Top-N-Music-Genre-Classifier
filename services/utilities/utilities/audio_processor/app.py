from typing import Iterable, Optional

import librosa
import numpy as np
from PIL import Image


def spectrogram_generator(
    file_path: str, desired_segments_seconds: int = 5, sample_rate: int = 22050
) -> Iterable[np.ndarray]:
    """
    Converts an audio stream to a mel spectrogram.

    :param file_path: Path to audio file
    :param desired_segments_seconds: Seconds of audio to slice when creating the mel spectrogram.
        Equal segments of this param value are made as the duration of the audio file allows.
    :return: Power Mel Spectrogram constructed from audio file with n_mels=128

    """

    audio_data, sr = librosa.load(
        file_path, sr=sample_rate, mono=True, duration=90
    )  # less is loaded if clip<duration but set 90 to max
    clip_duration = librosa.get_duration(y=audio_data, sr=sr)
    # available slices of desired_segments_seconds
    possible_segments = int(clip_duration / desired_segments_seconds)

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


def transform_spectrogram(spectrogram: np.ndarray) -> np.ndarray:
    """
    Applies standardization and contrast normalization to spectrogram.
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


def spectrogram_to_image(spectrogram: np.ndarray) -> Image:
    """Spectrogram array as image in greyscale standardized and contrast normalized.

    :param spectrogram: Spectrogram to be converted to image
    :return: spectrogram as PIL Image
    """

    rescaled = transform_spectrogram(spectrogram)
    image = Image.fromarray(rescaled, mode="L")
    return image


def log_spectrogram(mel_spectrogram: np.ndarray) -> np.ndarray:
    """Log mel spectrogram from spectrogram.
    In a log mel spectrogram, amplitude is converted to decibels which follows a logarithmic scale.

    :param mel_spectrogram: Mel spectrogram to be converted
    :return: Log Mel Spectrogram
    """
    log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
    return log_mel_spectrogram


def convert_sound_to_image(
    sound_file_path: str,
    librosa_options: Optional[dict] = None,
) -> Iterable[Image.Image]:
    """
     Interface for converting sound to image.
    Default librosa_options are: desired_segments_seconds: int = 5, sample_rate: int = 22050

    :param sound_file_path: Path to audio file
    :param librosa_options: Options used by Librosa for creating the spectrogram
    :return: Log Mel Spectrogram as PIL Image instance
    """
    spectrogram_gen = (
        spectrogram_generator(sound_file_path, **librosa_options)
        if librosa_options
        else spectrogram_generator(sound_file_path)
    )

    for spec in spectrogram_gen:
        log_spec = log_spectrogram(spec)
        image = spectrogram_to_image(log_spec)
        yield image
