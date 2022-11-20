from os import PathLike
from typing import Iterator, List, TypeAlias

import joblib
import librosa
import numpy as np
from numpy.typing import NDArray
from PIL import Image

PILImage: TypeAlias = Image.Image


def audio_slicer(
    file_path: str | PathLike,
    desired_segments_seconds: int = 5,
    sample_rate: int = 22050,
    duration: int = 90,
) -> List[NDArray]:
    """Converts an audio stream to a mel spectrogram.

    :param file_path: Path to audio file
    :param desired_segments_seconds: Seconds of audio to slice when creating the mel spectrogram.
        Equal segments of this param value are made as the duration of the audio file allows.
    :param sample_rate: Sample rate to down sample audio to, in Hz
    :param duration: How long of audio file to load. Less is loaded if clip length < duration
    :return: Power Mel Spectrogram constructed from audio file with n_mels=128
    """
    audio_data, sr = librosa.load(file_path, sr=sample_rate, mono=True, duration=duration)
    window_size = sr * desired_segments_seconds
    audio_windowed = np.array_split(
        audio_data, np.arange(window_size, audio_data.size, window_size)
    )
    # check for potential last window being too short
    if audio_windowed[-1].size != window_size:
        return audio_windowed[:-1]

    return audio_windowed


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
    return librosa.power_to_db(mel_spectrogram, ref=np.max)


def convert_sound_to_image(
    sound_file_path: str | PathLike, duration: int = 30, **librosa_options: int
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
    spectrogram_gen = audio_slicer(sound_file_path, **librosa_options)
    spectrogram = librosa.feature.melspectrogram(
        y=spectrogram_gen[0], hop_length=2048, sr=librosa_options.get("sample_rate", 22050)
    )
    log_spec = log_spectrogram(spectrogram)
    image = spectrogram_to_image(log_spec)
    return image


def generate_sound_images(
    sound_file_path: str | PathLike, n_threads: int = 2, **librosa_options: int
) -> Iterator[PILImage]:
    """Interface for converting sound to multiple images

    Default ``librosa_options`` are:
        * desired_segments_seconds: int = 5
        * sample_rate: int = 22050
        * duration: int = 30

    :param sound_file_path: Path to audio file
    :param n_threads: Number of threads to use when processing spectrogram
    :param librosa_options: Options used by Librosa for creating the spectrogram
    :return: Generator of Log Mel Spectrograms as PIL Image instances
    """
    spectrogram_gen = audio_slicer(sound_file_path, **librosa_options)

    def mapper(data):
        return spectrogram_to_image(
            log_spectrogram(
                librosa.feature.melspectrogram(
                    y=data,
                    sr=librosa_options.get("sample_rate", 22050),
                    n_mels=128,
                    hop_length=2048,
                )
            )
        )

    with joblib.parallel_backend(backend="threading", n_jobs=n_threads):
        output = joblib.Parallel()([joblib.delayed(mapper)(data) for data in spectrogram_gen])
        return output
