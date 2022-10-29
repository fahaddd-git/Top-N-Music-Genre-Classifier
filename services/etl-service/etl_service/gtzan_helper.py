from pathlib import Path
from typing import Iterable


class GtzanHelper:
    """
    Contains helper methods for working with the gtzan dataset.
    """

    def __init__(self, gtzan_dataset_dir: Path):
        """
        :param gtzan_dataset_dir: Path to the directory full of wav files.
        """
        if not gtzan_dataset_dir.exists():
            raise FileExistsError(gtzan_dataset_dir.absolute())
        self.gtzan_path = gtzan_dataset_dir

    @staticmethod
    def get_genre(gtzan_file_name: Path) -> str:
        """
        Returns the genre from the filename of an audio file from the gtzan
        dataset. Note the genre is the first part of the file name
        (e.g. "classical.00062.wav")
        :param gtzan_file_name: Path to an audio file from the gtzan dataset.
        """
        return gtzan_file_name.name.split(".", 1)[0]

    def get_genres(self) -> set:
        """
        :param gtzan_path: Path to the directory of GTZAN dataset of wav files
        :return: The set of all the genre names from the data set.
        """
        return set(self.get_genre(f) for f in self.gtzan_path.glob("*.wav"))

    def get_files(self) -> Iterable[Path]:
        """
        Returns a listing of the paths to all the .wav files.
        """
        return self.gtzan_path.glob("*.wav")
