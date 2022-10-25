from typing import Optional

import librosa
import librosa.display
import numpy as np
from PIL import Image


def stream_spectrogram(
    file_path: str, n_fft: int = 2048, hop_length: int = 2048, frame_length: int = 2048
) -> np.ndarray:
    """
    Converts an audio stream to a mel spectrogram by way of STFTs.
    An explanation of the reasoning behind this workflow can be found at
    https://dsp.stackexchange.com/questions/76637/do-mel-spectrograms-of-two-audios-have-linear-property

    :param file_path: Path to audio file
    :param n_fft: Length of the FFT window
    :param hop_length: Number of samples between successive frames
    :param frame_length: The number of samples per frame
    :return: Power Mel Spectrogram constructed from audio file with n_mels=128

    """

    stream = librosa.stream(
        file_path,
        block_length=256,  # buffer size
        frame_length=frame_length,
        hop_length=hop_length,
    )
    all_blocks = []
    for block in stream:
        curr_block = librosa.stft(y=block, n_fft=n_fft, hop_length=2048, center=False)

        all_blocks.append(curr_block)
    all_blocks = np.hstack(all_blocks)

    # https://librosa.org/doc/main/generated/librosa.feature.melspectrogram.html
    # convert stfts to mel spectrogram
    abs_value = np.abs(all_blocks) ** 2
    sr = librosa.get_samplerate(file_path)
    mel_spectro = librosa.feature.melspectrogram(
        S=abs_value, sr=sr, hop_length=2048, center=False, n_mels=128
    )

    return mel_spectro


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
    # https://stackoverflow.com/questions/70783357/how-do-i-normalize-the-pixel-value-of-an-image-to-01
    spec_scaled = (standardized - standardized_min) / (standardized.max() - standardized_min) * 255
    return spec_scaled.astype(np.uint8)


def spectrogram_to_image(spectrogram: np.ndarray) -> Image:
    """Spectrogram array as image in greyscale standardized and contrast normalized.

    :param spectrogram: Spectrogram to be converted to image
    :return: spectrogram as PIL Image
    """

    rescaled = transform_spectrogram(spectrogram)
    image = Image.fromarray(rescaled, mode="L")
    image.show()
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
) -> Image:
    """
     Interface for converting sound to image.
    Default librosa_options are: n_fft: int = 2048, hop_length: int = 2048, frame_length: int = 2048

    :param sound_file_path: Path to audio file
    :param librosa_options: Options used by Librosa for creating the spectrogram
    :return: Log Mel Spectrogram as PIL Image
    """
    spectrogram = (
        stream_spectrogram(sound_file_path, **librosa_options)
        if librosa_options
        else stream_spectrogram(sound_file_path)
    )
    log_spec = log_spectrogram(spectrogram)
    image = spectrogram_to_image(log_spec)
    return image
