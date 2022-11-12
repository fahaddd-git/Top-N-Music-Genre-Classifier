from pathlib import Path
from typing import Iterable

from etl_service.contracts.exceptions import IncorrectFilename


class DataSetHelper:
    """
    Contains helper methods for working with the gtzan dataset.
    """

    def __init__(self, data_set_dir: Path):
        """
        :param dataset_dir: Path to the directory full of wav files.
        """
        if not data_set_dir.exists():
            raise FileExistsError(data_set_dir.absolute())
        self.data_set_path = data_set_dir

    @staticmethod
    def get_genre(file_name: Path) -> str:
        """
        Returns the genre from the filename of an audio file from the gtzan
        dataset. Note the genre is the first part of the file name
        (e.g. "classical.00062.wav").

        :param gtzan_file_name: Path to an audio file from the gtzan dataset.
        :raises IncorrectFilename: If the file is not named correctly.
        """
        if file_name.name.count(".") != 2 or not file_name.name.endswith(".wav"):
            raise IncorrectFilename(f"{file_name} not named correctly (i.e. classical.00062.wav)")

        return file_name.name.split(".", 1)[0]

    def get_genres(self) -> set:
        """
        :param gtzan_path: Path to the directory of GTZAN dataset of wav files
        :return: The set of all the genre names from the data set.
        """
        genres = []
        for file in self.data_set_path.glob("*.wav"):
            try:
                genres.append(self.get_genre(file))
            except IncorrectFilename:
                continue
        return set(genres)

    def get_files(self) -> Iterable[Path]:
        """
        Returns a listing of the paths to all the .wav files.
        """
        return self.data_set_path.glob("*.wav")
