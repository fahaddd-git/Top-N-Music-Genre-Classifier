from sqlalchemy import Column, DateTime, ForeignKey, Integer, LargeBinary, Text
from sqlalchemy.orm import declarative_base, relationship

_BaseModel = declarative_base()


class Genre(_BaseModel):
    """Corresponds to ``genres`` table

    Columns:
        - id (pk, integer)
        - name (text, unique)
    .
    Relationships:
        - Spectrogram (on Genre.id == Spectrogram.genre_id)
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
        - Genre (on Spectrogram.genre_id == Genre.id)
    """

    __tablename__ = "spectrograms"

    id = Column(Integer, primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    image_data = Column(LargeBinary, nullable=False)
    last_modified = Column(DateTime, nullable=False)

    genre = relationship("Genre", back_populates="spectrograms")
