from pathlib import Path

import pytest
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
        (Path("metal.00063.mp3"), "metal"),
        (Path("metal.foo.bar"), "metal"),
    ],
)
def test_get_genre_expected_file_name(file_name: Path, genre: str):
    assert DataSetHelper.get_genre(file_name) == genre


def test_get_genres_expected_file_names(tmp_path):
    (tmp_path / "classical.00062.wav").touch()
    (tmp_path / "classical.00063.wav").touch()
    (tmp_path / "blues.00062.wav").touch()
    (tmp_path / "blues.00063.wav").touch()
    (tmp_path / "metal.00063.mp3").touch()
    (tmp_path / "metal.foo.wav").touch()
    (tmp_path / "pop.00062.foo").touch()
    (tmp_path / "pop.00063.foo").touch()
    data_set_helper = DataSetHelper(tmp_path)

    genres = data_set_helper.get_genres()

    assert genres == set(("classical", "blues", "metal"))


def test_get_files_expected_file_names(tmp_path):
    expected_files = [
        tmp_path / "classical.00062.wav",
        tmp_path / "classical.00063.wav",
        tmp_path / "blues.00062.wav",
        tmp_path / "blues.00063.wav",
        tmp_path / "metal.00063.mp3",
        tmp_path / "metal.foo.wav",
        tmp_path / "pop.00062.foo",
        tmp_path / "pop.00063.foo",
    ]
    for file in expected_files:
        file.touch()
    data_set_helper = DataSetHelper(tmp_path)

    actual_files = data_set_helper.get_files()

    assert sorted(actual_files) == sorted(f for f in expected_files if f.name.endswith(".wav"))
