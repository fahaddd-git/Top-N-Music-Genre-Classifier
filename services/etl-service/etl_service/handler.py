from datetime import datetime
from typing import Any, Callable

from etl_service.file_convertor import FileConvertor
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from utilities.db.connector import sqlite_session
from utilities.db.models import Genre, Spectrogram


def handle(file_converter: FileConvertor, callback: Callable[[int], Any] | None = None):
    """Handles the ETL process, converting and loading files to the database until all
    files are processed

    :param file_converter: instance of FileConverter
    :param callback: called with the number of spectrograms processed (return value ignored)
    """
    with sqlite_session().begin() as session:
        for num_processed, spectrogram in enumerate(file_converter.convert_files(), start=1):
            try:
                genre = session.execute(
                    select(Genre).filter_by(name=spectrogram.genre)
                ).scalar_one()
            except NoResultFound:
                genre = Genre(name=spectrogram.genre)
                session.add(genre)
                genre = session.execute(
                    select(Genre).filter_by(name=spectrogram.genre)
                ).scalar_one()

            session.add(
                Spectrogram(
                    image_data=spectrogram.image_stream,
                    genre_id=genre.id,
                    last_modified=datetime.now(),
                )
            )
            if callable(callback):
                callback(num_processed)
