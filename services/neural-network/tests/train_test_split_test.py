import unittest

from neural_network.train_test_split import train_test_split


# This test will obviously fail if we modify our database
class TrainTestSplit(unittest.TestCase):
    def test_varying_train_fraction_length_partitions(self):
        # train_fraction, expected_num_train, expected_num_test
        params = [
            (0.5, 500, 500),
            (0.6, 600, 400),
            (0.4, 400, 600),
            (0.75, 750, 250),
            (0.813, 820, 180),
        ]

        for train_fraction, num_train, num_test in params:
            with self.subTest():
                spectrogram_data = train_test_split(train_fraction)
                self.assertEqual(len(spectrogram_data.train_data), num_train)
                self.assertEqual(len(spectrogram_data.train_labels), num_train)
                self.assertEqual(len(spectrogram_data.test_data), num_test)
                self.assertEqual(len(spectrogram_data.test_labels), num_test)

    def test_labels_are_correct(self):
        expected_labels = [
            *[1] * 50,
            *[2] * 50,
            *[3] * 50,
            *[4] * 50,
            *[5] * 50,
            *[6] * 50,
            *[7] * 50,
            *[8] * 50,
            *[9] * 50,
            *[10] * 50,
        ]

        spectrogram_data = train_test_split(train_fraction=0.5)
        self.assertListEqual(spectrogram_data.train_labels, expected_labels)
        self.assertListEqual(spectrogram_data.test_labels, expected_labels)
