import unittest

# from neural_network.data_ingestion_helpers import get_genre_occurrences
from neural_network.data_ingestion_helpers import train_test_split
from utilities.db.connector import sqlite_session
from utilities.db.models import Spectrogram


class TrainTestSplit(unittest.TestCase):
    def setUp(self):
        with sqlite_session().begin() as session:
            self.num_spectrograms = session.query(Spectrogram).count()

    def test_varying_train_fraction_length_partitions(self):
        n = self.num_spectrograms
        params = [
            (0.5, 0.5 * n, 0.5 * n),
            (0.6, 0.6 * n, 0.4 * n),
            (0.4, 0.4 * n, 0.6 * n),
            (0.75, 0.75 * n, 0.25 * n),
            (0.813, 0.82 * n, 0.18 * n),
        ]

        for train_fraction, num_train, num_test in params:
            with self.subTest():
                spectrogram_data = train_test_split(train_fraction)
                self.assertEqual(len(spectrogram_data.train_data), num_train)
                self.assertEqual(len(spectrogram_data.train_labels), num_train)
                self.assertEqual(len(spectrogram_data.test_data), num_test)
                self.assertEqual(len(spectrogram_data.test_labels), num_test)

    # def test_labels_are_correct(self):
    #     occurances = get_genre_occurrences()
    #     print(occurances)
    #     expected_labels = []
    #     for label, count in occurances.items():
    #         for i in range(count):
    #             expected_labels.append(label - 1)

    #     spectrogram_data = train_test_split(train_fraction=0.5)
    #     self.assertEqual(spectrogram_data.train_labels, expected_labels)
    #     self.assertEqual(spectrogram_data.test_labels, expected_labels)
