from datetime import datetime

from etl_service.file_convertor import FileConvertor
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from utilities.db.connector import sqlite_session
from utilities.db.models import Genre, Spectrogram


def handle(file_converter: FileConvertor) -> int:
    """Handles the ETL process, converting and loading files to the database until all
    files are processed

    :return: number of spectrograms added
    """
    spectrograms_processed = 0
    with sqlite_session().begin() as session:
        for spectrogram in file_converter.convert_files():
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
            spectrograms_processed += 1
        return spectrograms_processed
