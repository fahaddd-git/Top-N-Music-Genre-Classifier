import io
from typing import TypeAlias

from PIL import Image, UnidentifiedImageError
from sqlalchemy import Column, DateTime, ForeignKey, Integer, LargeBinary, Text
from sqlalchemy.orm import declarative_base, relationship

PILImage: TypeAlias = Image.Image | None

_BaseModel = declarative_base()


class Genre(_BaseModel):
    """Corresponds to ``genres`` table

    Columns:
        - id (pk, integer)
        - name (text, unique)

    Relationships:
        - spectrograms (on Genre.id == Spectrogram.genre_id)
    """

    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)

    spectrograms = relationship("Spectrogram", back_populates="genre")


class Spectrogram(_BaseModel):
    """Corresponds to ``spectrograms`` table

    Columns:
        - id (pk, integer)
        - genre_id (fk, integer)
        - image_data (blob)
        - last_modified (datetime)

    Relationships:
        - genre (on Spectrogram.genre_id == Genre.id)
    """

    __tablename__ = "spectrograms"

    id = Column(Integer, primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    image_data = Column(LargeBinary, nullable=False)
    last_modified = Column(DateTime, nullable=False)

    genre = relationship("Genre", back_populates="spectrograms")

    @property
    def image(self) -> PILImage:
        """Spectrogram data as a PIL Image (None if data cannot be read as an image)"""
        buffer = io.BytesIO(self.image_data)
        try:
            return Image.open(buffer)
        except UnidentifiedImageError:
            pass  # todo: log error
        return None

    @property
    def grayscale_image(self) -> PILImage:
        """Spectrogram image coerced to grayscale (None if data cannot be read as an image)"""
        return image.convert("L") if (image := self.image) else None
