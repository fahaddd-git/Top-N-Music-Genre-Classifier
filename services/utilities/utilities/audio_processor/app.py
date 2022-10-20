from os import makedirs

import librosa
import librosa.display

# import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

filename = "tests/test_files/classical.00000.wav"


def stream_spectrogram(file_path, n_fft=2048, hop_length=2048, frame_length=2048):
    """
    Converts an audio stream to a mel spectrogram by way of STFTs.
    An explanation of the reasoning behind this workflow can be found at
    https://dsp.stackexchange.com/questions/76637/do-mel-spectrograms-of-two-audios-have-linear-property

    :param file_path: Path to audio file
    :type file_path: str
    :param n_fft: Length of the FFT window
    :type n_fft: int, optional
    :param hop_length: Number of samples between successive frames
    :type hop_length: int, optional
    :param frame_length: The number of samples per frame
    :type frame_length: int, optional

    :return: Power Mel Spectrogram constructed from audio file with n_mels=128
    :rtype: numpy.ndarray
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

    # displays mel spectrogram
    # librosa.display.specshow(mel_spectro, sr=sr, x_axis="time", y_axis="mel", hop_length=2048)
    # plt.colorbar()
    # plt.show()

    return mel_spectro


def transform_spectrogram(spectrogram):
    """
    Applies standardization and contrast normalization to spectrogram.
    This is so that the spectrogram, a numpy array, can be cast as a greyscale image.

    :param spectrogram: Spectrogram to be transformed
    :type spectrogram: numpy.ndarray

    :return: Standardized and Normalized spectrogram.  All values between [0-255]
    :rtype: numpy.ndarray(type=uint8)
    """
    # standardize data https://en.wikipedia.org/wiki/Standard_score
    standardized = (spectrogram - spectrogram.mean()) / spectrogram.std()
    standardized_min = standardized.min()
    # contrast normalization for greyscale image
    # https://stackoverflow.com/questions/70783357/how-do-i-normalize-the-pixel-value-of-an-image-to-01https://stackoverflow.com/questions/70783357/how-do-i-normalize-the-pixel-value-of-an-image-to-01
    spec_scaled = (standardized - standardized_min) / (standardized.max() - standardized_min) * 255
    return spec_scaled.astype(np.uint8)


def save_spectrogram_to_image(spectrogram, file_name, file_path="utilities/audio_processor/images"):
    """Saves spectrogram as .png file in greyscale

    :param spectrogram: Spectrogram to be saved as .png
    :type spectrogram: numpy.ndarray
    :param file_name: Name of file to be saved without extension
    :type file_name: str
    :param file_path: Where to save the image file:
    :type file_path: str, optional

    :return: None, Image saved to file_path with file_name as .png
    :rtype: NoneType
    """

    rescaled = transform_spectrogram(spectrogram)
    makedirs(file_path, exist_ok=True)
    image = Image.fromarray(rescaled)
    image.save(f"{file_path}/{file_name}.png")


def log_spectrogram(mel_spectrogram):
    """Returns log mel spectrogram.
    In a log mel spectrogram, amplitude is converted to decibels which follows a logarithmic scale.

    :param mel_spectrogram: Mel spectrogram to be converted
    :type mel_spectrogram: numpy.ndarray

    :return: Log Mel Spectrogram
    :rtype: numpy.ndarray
    """
    log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

    return log_mel_spectrogram
