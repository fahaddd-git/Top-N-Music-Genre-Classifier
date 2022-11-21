import pytest


@pytest.fixture()
def genres():
    return {"classical", "blues", "metal", "pop"}


@pytest.fixture()
def files_happy_path():
    return [
        "classical.00062.wav",
        "classical.00063.wav",
        "blues.00062.wav",
        "blues.00063.wav",
        "metal.00062.wav",
        "metal.00063.wav",
        "pop.00062.wav",
        "pop.00063.wav",
    ]


@pytest.fixture()
def files_unknown_extensions():
    return [
        "classical.00062.mp3",
        "classical.00063.mp4",
        "blues.00062.ogg",
        "blues.00063.foo",
        "metal.00062.bar",
        "metal.00063.wma",
        "pop.00062.aac",
        "pop.00063.aiff",
    ]
