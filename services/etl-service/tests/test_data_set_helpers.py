from pathlib import Path

import pytest
from etl_service.contracts.exceptions import IncorrectFilename
from etl_service.data_set_helper import DataSetHelper


def test_instantiate_existant_directory_no_errors(tmp_path):
    gtzan_helper = DataSetHelper(tmp_path)
    assert gtzan_helper.data_set_path == tmp_path


def test_instantiate_non_existant_directory_throws_error(tmp_path):
    tmp_path.rename(tmp_path.parent / "non_existant")

    with pytest.raises(FileExistsError):
        gtzan_helper = DataSetHelper(tmp_path)
        assert gtzan_helper.data_set_path == tmp_path


@pytest.mark.parametrize(
    "file_name,genre",
    [
        (Path("classical.00062.wav"), "classical"),
        (Path("classical.00063.wav"), "classical"),
        (Path("blues.00062.wav"), "blues"),
        (Path("blues.00063.wav"), "blues"),
    ],
)
def test_get_genre_expected_file_name(file_name: Path, genre: str):
    assert DataSetHelper.get_genre(file_name) == genre


@pytest.mark.parametrize(
    "file_name",
    [
        Path("metal"),
        Path("metal.wav"),
        Path("metal.00063.mp3"),
        Path("foo.bar.baz"),
    ],
)
def test_get_genre_bad_file_name(file_name: Path):
    with pytest.raises(IncorrectFilename):
        DataSetHelper.get_genre(file_name)


def test_get_genres_expected_file_names(tmp_path, files_happy_path, genres):
    for name in files_happy_path:
        (tmp_path / name).touch()
    data_set_helper = DataSetHelper(tmp_path)

    actual_genres = data_set_helper.get_genres()

    assert actual_genres == genres


def test_get_genres_unknown_extensions(tmp_path, files_unknown_extensions):
    for name in files_unknown_extensions:
        (tmp_path / name).touch()

    data_set_helper = DataSetHelper(tmp_path)

    genres = data_set_helper.get_genres()
    assert genres == set()


def test_get_genres_unknown_files_skipped(
    tmp_path, files_happy_path, files_unknown_extensions, genres
):
    for name in [*files_happy_path, *files_unknown_extensions]:
        (tmp_path / name).touch()

    data_set_helper = DataSetHelper(tmp_path)

    genres = data_set_helper.get_genres()
    assert genres == genres


def test_get_files_expected_file_names(tmp_path, files_happy_path):
    expected_files = [tmp_path / name for name in files_happy_path]
    for file in expected_files:
        file.touch()
    data_set_helper = DataSetHelper(tmp_path)

    actual_files = data_set_helper.get_files()

    assert sorted(actual_files) == sorted(expected_files)


def test_get_files_unexpected_file_names(tmp_path, files_unknown_extensions):
    expected_files = [tmp_path / name for name in files_unknown_extensions]
    for file in expected_files:
        file.touch()
    data_set_helper = DataSetHelper(tmp_path)

    actual_files = data_set_helper.get_files()

    assert list(actual_files) == []
