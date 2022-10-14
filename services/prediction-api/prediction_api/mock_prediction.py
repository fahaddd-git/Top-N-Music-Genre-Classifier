from random import random

all_genres = [
    "blues",
    "rap",
    "rock",
    "jazz",
    "hiphop",
    "hip hop",
    "r&b",
    "folk",
    "alternative",
]


def predict(file: bytes) -> dict:
    return {genre: random() for genre in all_genres}
