import io
from datetime import datetime
from pathlib import Path
from typing import Final
from unittest.mock import patch

import pytest
from PIL import Image, UnidentifiedImageError
from utilities.db.models import Spectrogram

MODULE_PATH: Final = "utilities.db.models"
SAMPLE_IMAGE_PATH: Final = Path(__file__).resolve().parent / "test_files/blues.00036.png"


@pytest.fixture(scope="session")
def spectrogram_with_image() -> tuple[Spectrogram, Image.Image]:
    buffer = io.BytesIO()
    with open(SAMPLE_IMAGE_PATH, "rb") as png_image:
        buffer.write(png_image.read())
    spectrogram = Spectrogram(
        id=1, genre_id=1, image_data=buffer.getvalue(), last_modified=datetime.now()
    )
    image = Image.open(buffer)
    return spectrogram, image


def assert_images_equal(first_image: Image.Image, second_image: Image.Image):
    first_image_data = first_image.getdata()
    second_image_data = second_image.getdata()
    assert first_image.size == second_image.size
    assert all(
        first_pixel == second_pixel
        for first_pixel, second_pixel in zip(first_image_data, second_image_data)
    )


def test_spectrogram_image(spectrogram_with_image):
    spectrogram, original_image = spectrogram_with_image
    assert_images_equal(spectrogram.image, original_image)


def test_spectrogram_grayscale(spectrogram_with_image):
    spectrogram, original_image = spectrogram_with_image
    assert_images_equal(spectrogram.grayscale_image, original_image.convert("L"))


@patch(f"{MODULE_PATH}.Image.open")
def test_spectrogram_image_returns_none_if_cannot_be_read(patched_open, spectrogram_with_image):
    spectrogram, _ = spectrogram_with_image
    patched_open.side_effect = UnidentifiedImageError
    assert spectrogram.image is None
    assert spectrogram.grayscale_image is None
