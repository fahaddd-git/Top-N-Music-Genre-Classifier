from pathlib import Path
from utilities.db.connector import sqlite_session
from utilities.db.models import Genre, Spectrogram
from gtzan_helper import GtzanHelper
from file_convertor import FileConvertor
from sqlalchemy import select
from sqlalchemy.orm import SessionTransaction
from sqlalchemy.exc import NoResultFound
from datetime import datetime
import time

# check the unprocessed directory for newly added files every 60 seconds
num_seconds_to_sleep = 60

# path to the gtzan dataset of .wav files. This in theory should process any
# example .wav file that is named in the same fashion as the gtzan dataset.
gtzan = GtzanHelper(Path().home() / "gtzan")

# processed files will end up in $HOME/gtzan/processed
file_converter = FileConvertor(gtzan)

# log number of files processed to STDOUT
spectrograms_processed = 0

session: SessionTransaction
with sqlite_session().begin() as session:
    while True:
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

            session.add(Spectrogram(
                image_data=bytes(spectrogram.image.tobytes()),
                genre_id=genre.id,
                last_modified=datetime.now(),
            ))
            print("Spectrogram processed", spectrograms_processed)
            spectrograms_processed += 1

        # watch for any newly added unprocessed files
        print("Sleeping for", num_seconds_to_sleep, "seconds")
        time.sleep(num_seconds_to_sleep)
