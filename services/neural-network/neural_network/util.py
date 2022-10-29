import io

import numpy as np
from PIL import Image
from sqlalchemy.orm import SessionTransaction
from utilities.db.connector import sqlite_session
from utilities.db.models import Genre


def image_to_array(image: bytes) -> np.ndarray:
    image_buffer = io.BytesIO(image)
    image = Image.open(image_buffer)
    return np.array(image)


def get_labels() -> dict:
    session: SessionTransaction  # so I can get lsp autocompletion
    with sqlite_session().begin() as session:
        genres = session.query(Genre).all()
        return {g.id: g.name for g in genres}


if __name__ == "__main__":
    print(get_labels())
