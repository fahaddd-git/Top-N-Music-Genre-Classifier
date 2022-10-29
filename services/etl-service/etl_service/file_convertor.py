import io

from dataclasses import dataclass
from gtzan_helper import GtzanHelper
from pathlib import Path
from typing import Iterable
from utilities.audio_processor import convert_sound_to_image


@dataclass
class SpectrogramData:
    image_stream: bytes
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
            image_stream = io.BytesIO()
            image = convert_sound_to_image(file)
            image.save(image_stream, format="png")

            file.rename(self.processed_dir / file.name)
            genre = self.gtzan_helper.get_genre(file)
            spectrogram = SpectrogramData(image_stream.getvalue(), genre)
            yield spectrogram
