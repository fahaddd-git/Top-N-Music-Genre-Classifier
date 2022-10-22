from typing import Final
from unittest.mock import AsyncMock, MagicMock, Mock, PropertyMock, patch

import pytest
from fastapi import HTTPException, UploadFile
from prediction_api.routers.predict_genre import (
    SUPPORTED_AUDIO_CONTENT_SUBTYPES,
    is_supported_audio_file,
    predict_genre,
)

MODULE_PATH: Final = "prediction_api.routers.predict_genre"


@pytest.fixture(scope="function")
def mock_upload_files(request) -> tuple[Mock, Mock]:
    """Return mocked UploadFiles (extra params unset, extra params set) from the passed mime type"""
    # see https://docs.pytest.org/en/stable/example/parametrize.html (apply indirect)
    without_extra, with_extra = Mock(spec_set=UploadFile), Mock(spec_set=UploadFile)
    type(without_extra).content_type = PropertyMock(return_value=f"audio/{request.param}")
    type(with_extra).content_type = PropertyMock(return_value=f"audio/{request.param};param=val")
    return without_extra, with_extra


@pytest.mark.parametrize("mock_upload_files", SUPPORTED_AUDIO_CONTENT_SUBTYPES, indirect=True)
def test_is_supported_audio_file_on_valid_types(mock_upload_files):
    assert all(is_supported_audio_file(file) for file in mock_upload_files)


@pytest.mark.parametrize(
    "content_type",
    [
        pytest.param("audio/jpeg", id="Unsupported audio subtype"),
        pytest.param("text/wav", id="Unsupported mime type"),
        pytest.param("audio/", id="Missing audio subtype"),
        pytest.param("audio", id="Invalid formatting"),
        pytest.param("", id="Empty string"),
    ],
)
def test_is_supported_audio_file_on_invalid_types(content_type):
    mock_file = Mock(spec_set=UploadFile)
    type(mock_file).content_type = PropertyMock(return_value=content_type)
    assert not is_supported_audio_file(mock_file)


@pytest.mark.anyio
@patch(f"{MODULE_PATH}.is_supported_audio_file")
async def test_predict_genre_raises_http_exception(patched_is_supported_audio_file):
    patched_is_supported_audio_file.return_value = False
    file = UploadFile(filename="apricot.wav")
    with pytest.raises(HTTPException):
        await predict_genre(file)


@pytest.mark.anyio
@patch(f"{MODULE_PATH}.is_supported_audio_file")
@patch(f"{MODULE_PATH}.predict")
async def test_predict_genre(patched_predict, patched_is_supported_audio_file):
    patched_is_supported_audio_file.return_value = True
    patched_predict.return_value = {"genre": 0.10}
    filestream = MagicMock(spec_set=bytes)
    file = MagicMock(spec_set=UploadFile, read=AsyncMock(return_value=filestream))

    result = await predict_genre(file)

    file.read.assert_called_once()
    patched_predict.assert_called_once_with(filestream)
    assert result is patched_predict.return_value
