from math import ceil

# import numpy as np
from PIL.Image import Image
from sqlalchemy import func  # , select
from utilities.db.connector import sqlite_session
from utilities.db.models import Genre, Spectrogram

# from typing import Iterable


def _get_genre_occurances() -> dict:
    occurances = {}
    with sqlite_session().begin() as session:
        genres = session.query(Genre).all()
        for genre in genres:
            occurances[genre.id] = 0

        for genres in genres:
            genre_count = session.query(func.count(Spectrogram.genre_id)).scalar()
            occurances[genres.id] = genre_count

        return occurances


def train_test_split(train_fraction=0.8) -> (list[Image], list[str], list[Image], list[str]):
    if 1 <= train_fraction <= 0:
        raise Exception("Train fraction must be between 0 and 1")
    # test_fraction = 1 - train_fraction
    genre_occurances = _get_genre_occurances()

    train_results = []
    test_results = []
    with sqlite_session().begin() as session:
        for genre_id, num_examples in genre_occurances.items():
            num_train = ceil(num_examples * train_fraction)
            # num_test = ceil(num_examples * test_fraction)

            train_results += (
                session.query(Spectrogram)
                .filter(Spectrogram.genre_id == genre_id)
                .limit(num_train)
                .all()
            )

            # test_results.append(
            #     session
            #     .query(Spectrogram)
            #     .filter(genre_id=genre_id)
            #     .skip(num_train)
            #     .limit(num_test)
            #     .all()
            # )

        # # base_query = """
        # # select g.name, s.image from genres g
        # # inner join spectrograms s on g.id = s.genreID
        # # where g.name like ?
        # # """
        # # train_query = base_query + f"limit {num_train}"
        # # test_query = base_query + f"limit {num_test} offset {num_train}"

        # train_data = cursor\
        #     .execute(train_query, [f"%{genre_id}%"])\
        #     .fetchall()
        # test_data = cursor\
        #     .execute(test_query, [f"%{genre_id}%"])\
        #     .fetchall()

        # train_results.append(train_data)
        # test_results.append(test_data)

    return train_results, test_results


# def _flatten(lst: list):
#     flattened_list = []
#     for sub_list in lst:
#         for item in sub_list:
#             flattened_list.append(item)
#     return flattened_list


if __name__ == "__main__":
    print(_get_genre_occurances())
    print(train_test_split())
