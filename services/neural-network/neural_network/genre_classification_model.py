from pathlib import Path

import tensorflow as tf
from neural_network.data_ingestion_helpers import SpectrogramData


class GenreClassificationModel:
    """A genre classification neural network tensorflow model"""

    def __init__(self, spectrogram_data: SpectrogramData):
        self._spectrogram_data = spectrogram_data
        self._model = tf.keras.models.Sequential()
        self._add_preprocessing_layers()
        self._add_normalization_layers()
        self._add_convolutional_layers()
        self._compile()

    def _add_preprocessing_layers(self) -> None:
        """Preprocess and attach input tensor"""
        # Currently, most images are approx 128x323 to 128x326, for an aspect ratio of about 0.4;
        # ideally, this logic should be made dynamic, but for now we can resize to 100x250
        resize_to_dimension = (100, 250)
        self._model.add(
            tf.keras.layers.Resizing(
                *resize_to_dimension,
                interpolation="area",
                input_shape=(*resize_to_dimension, 1),  # assume single-channel grayscale
                name="ResizeImages",
            )
        )

    def _add_normalization_layers(self) -> None:
        """Attach normalization tensors"""
        pass  # todo: normalize to be in 0..1 here; consider moving

    def _add_convolutional_layers(self) -> None:
        """Attach convolutional layers"""
        # Adapted from https://www.tensorflow.org/tutorials/audio/simple_audio
        # https://www.tensorflow.org/tutorials/audio/simple_audio
        self._model.add(tf.keras.layers.Conv2D(32, 3, activation="relu")),
        self._model.add(tf.keras.layers.MaxPooling2D()),
        self._model.add(tf.keras.layers.BatchNormalization())

        self._model.add(tf.keras.layers.Conv2D(32, 3, activation="relu")),
        self._model.add(tf.keras.layers.MaxPooling2D()),
        self._model.add(tf.keras.layers.BatchNormalization()),

        self._model.add(tf.keras.layers.Conv2D(32, 3, activation="relu")),
        self._model.add(tf.keras.layers.MaxPooling2D()),
        self._model.add(tf.keras.layers.BatchNormalization()),

        self._model.add(tf.keras.layers.Dropout(0.25)),
        self._model.add(tf.keras.layers.Flatten()),
        self._model.add(tf.keras.layers.Dense(128, activation="relu")),
        self._model.add(tf.keras.layers.Dropout(0.5)),
        self._model.add(
            tf.keras.layers.Dense(self._spectrogram_data.number_of_labels, activation="softmax")
        )

    def _compile(self) -> None:
        self._model.compile(
            optimizer="adam",
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=["accuracy"],  # track fraction correctly identified
        )

    def fit(self, epochs: int) -> None:
        self._model.fit(
            *self._spectrogram_data.train_dataset,
            batch_size=16,
            epochs=epochs,
            verbose=2
            # callbacks=tf.keras.callbacks.EarlyStopping(verbose=1, patience=2),
        )

    def evaluate(self):
        pass

    def save(self, file_path: Path) -> None:
        tf.keras.models.save_model(self._model, file_path)

    def load(self, file_path: Path) -> None:
        pass
