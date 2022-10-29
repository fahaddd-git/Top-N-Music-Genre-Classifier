from pathlib import Path
from utilities.db.connector import sqlite_session
from utilities.db.models import Genre, Spectrogram
from gtzan_helper import GtzanHelper
from file_convertor import FileConvertor
from sqlalchemy import select
from sqlalchemy.orm import SessionTransaction
from sqlalchemy.exc import NoResultFound
from datetime import datetime

gtzan = GtzanHelper(Path().home() / "gtzan")
file_converter = FileConvertor(gtzan)

session: SessionTransaction
with sqlite_session().begin() as session:
    for spectrogram in file_converter.convert_files():
        try:
            genre = session.execute(
                select(Genre).filter_by(name=spectrogram.genre)).scalar_one()
        except NoResultFound:
            genre = Genre(name=spectrogram.genre)
            session.add(genre)
            genre = session.execute(
                select(Genre).filter_by(name=spectrogram.genre)).scalar_one()

        session.add(Spectrogram(
            image_data=bytes(spectrogram.image.tobytes()),
            genre_id=genre.id,
            last_modified=datetime.now(),
        ))
