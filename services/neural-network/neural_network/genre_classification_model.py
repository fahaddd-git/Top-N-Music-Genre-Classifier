from os import PathLike
from pathlib import Path

import tensorflow as tf
from neural_network.data_ingestion_helpers import SpectrogramData
from numpy.typing import NDArray


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
            )
        )

    def _add_normalization_layers(self) -> None:
        """Attach normalization tensors"""
        pass

    def _add_convolutional_layers(self) -> None:
        """Attach convolutional layers"""
        # Adapted from the following sources:
        #   https://www.tensorflow.org/tutorials/audio/simple_audio
        #   https://www.tensorflow.org/tutorials/images/data_augmentation#train_a_model
        # Date: 11/3/2022
        self._model.add(tf.keras.layers.Conv2D(32, 3, activation="relu")),
        self._model.add(tf.keras.layers.MaxPooling2D(3, padding="same")),
        self._model.add(tf.keras.layers.BatchNormalization())

        self._model.add(tf.keras.layers.Conv2D(32, 3, activation="relu")),
        self._model.add(tf.keras.layers.MaxPooling2D(3, padding="same")),
        self._model.add(tf.keras.layers.BatchNormalization())

        self._model.add(tf.keras.layers.Conv2D(32, 3, activation="relu")),
        self._model.add(tf.keras.layers.MaxPooling2D(3, padding="same")),
        self._model.add(tf.keras.layers.BatchNormalization())

        self._model.add(tf.keras.layers.Flatten()),
        self._model.add(tf.keras.layers.Dense(128, activation="relu")),
        self._model.add(tf.keras.layers.Dropout(0.3)),
        self._model.add(
            tf.keras.layers.Dense(
                self._spectrogram_data.number_of_labels,
                activation="softmax",  # coerce to 0..1
                name="softmax_output_layer",
            )
        )

    def _compile(self) -> None:
        """Compile the model. Must be called after all layers have been attached."""
        self._model.compile(
            optimizer="adam",
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
            metrics=["accuracy"],  # track fraction correctly identified
        )

    def fit(self, epochs: int) -> None:
        """Fit the model based on the initial SpectrogramData"""
        self._model.fit(
            *self._spectrogram_data.train_dataset,
            batch_size=32,
            epochs=epochs,
            verbose="auto",
            # callbacks=tf.keras.callbacks.EarlyStopping(verbose=1, patience=2),
        )

    def evaluate(self) -> dict:
        """Evaluate the model based on its initial SpectrogramData"""
        metrics = self._model.evaluate(
            *self._spectrogram_data.test_dataset,
            verbose=2,
            return_dict=True,
        )
        return metrics

    def predict(self, tensor: tf.RaggedTensor) -> NDArray:
        """Predict from a **stack** RaggedTensor representing single-channel grayscale images"""
        return self._model.predict(tensor)

    def save(self, directory: str | PathLike) -> None:
        """Outputs the model in its current state to the specified output directory. If the path
        does not already exist, it is created. Any existing files are overwritten.
        """
        path = Path(directory).resolve()
        path.mkdir(parents=True, exist_ok=True)
        tf.keras.models.save_model(self._model, path, overwrite=True)
