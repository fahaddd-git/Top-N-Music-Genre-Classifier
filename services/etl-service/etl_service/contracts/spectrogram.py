from dataclasses import dataclass


@dataclass
class Spectrogram:
    image_stream: bytes
    genre: str
