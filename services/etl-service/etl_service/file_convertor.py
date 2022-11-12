import io
from pathlib import Path
from typing import Iterable

from data_set_helper import DataSetHelper
from etl_service.contracts.spectrogram import Spectrogram
from utilities.audio_processor import convert_sound_to_image


class FileConvertor:
    """
    Helps to convert the unprocessed gtzan dataset of wav files from
    the file system into images.
    """

    def __init__(self, data_set_helper: DataSetHelper, processed_dir: Path = None):
        """
        :param gtzan_helper: an instance of the DataSetHelper class
        :param processed_dir: a directory where the wav file will end up after
        they are processed.
        """
        if processed_dir is None:
            processed_dir = data_set_helper.data_set_path / "processed"
            processed_dir.mkdir(exist_ok=True)
        elif not processed_dir.exists():
            processed_dir.mkdir()
        self.processed_dir = processed_dir
        self.data_set_helper = data_set_helper

    def convert_files(self) -> Iterable[Spectrogram]:
        """
        Converts any unprocessed wav files in the gtzan dataset directory
        into an image, moves it to the processed directory, and returns the
        processed images.
        """
        for file in self.data_set_helper.get_files():
            image_stream = io.BytesIO()
            image = convert_sound_to_image(file)
            image.save(image_stream, format="png")

            file.rename(self.processed_dir / file.name)
            genre = self.data_set_helper.get_genre(file)
            spectrogram = Spectrogram(image_stream.getvalue(), genre)
            yield spectrogram
