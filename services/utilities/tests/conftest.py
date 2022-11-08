from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def sample_image_path() -> Path:
    return Path(__file__).resolve().parent / "fixtures/blues.00036.png"


@pytest.fixture(scope="session")
def sample_wav_path() -> Path:
    return Path(__file__).resolve().parent / "fixtures/classical.00000.wav"
