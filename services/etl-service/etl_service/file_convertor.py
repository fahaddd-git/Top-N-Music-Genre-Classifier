from typing import Iterable
from PIL.Image import Image
from pathlib import Path
from gtzan_helper import GtzanHelper
from utilities.audio_processor import convert_sound_to_image
from dataclasses import dataclass


@dataclass
class SpectrogramData:
    image: Image
    genre: str


class FileConvertor:
    """
    Helps to convert the unprocessed gtzan dataset of wav files from
    the file system into images.
    """

    def __init__(self, gtzan_helper: GtzanHelper, processed_dir: Path = None):
        """
        :param gtzan_helper: an instance of the GtzanHelper class
        :param processed_dir: a directory where the wav file will end up after
        they are processed.
        """
        if processed_dir is None:
            processed_dir = gtzan_helper.gtzan_path / "processed"
            processed_dir.mkdir(exist_ok=True)
        elif not processed_dir.exists():
            processed_dir.mkdir()
        self.processed_dir = processed_dir
        self.gtzan_helper = gtzan_helper

    def convert_files(self) -> Iterable[SpectrogramData]:
        """
        Converts any unprocessed wav files in the gtzan dataset directory
        into an image, moves it to the processed directory, and returns the
        processed images.
        """
        for file in self.gtzan_helper.get_files():
            image = convert_sound_to_image(file)
            file.rename(self.processed_dir / file.name)
            genre = self.gtzan_helper.get_genre(file)
            spectrogram = SpectrogramData(image, genre)
            yield spectrogram
