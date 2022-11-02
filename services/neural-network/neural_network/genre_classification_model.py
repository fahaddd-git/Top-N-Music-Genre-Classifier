from pathlib import Path

import tensorflow as tf
from neural_network.data_ingestion_helpers import SpectrogramData


class GenreClassificationModel:
    def __init__(self, spectrogram_data: SpectrogramData, labels: dict):
        self.labels = labels
        self._spectrogram_data = spectrogram_data
        self._model = tf.keras.models.Sequential()

        self._add_preprocessing_layers()
        self._add_normalization_layers()
        self._add_convolutional_layers()
        self._compile()

    def _add_preprocessing_layers(self) -> None:
        pass

    def _add_normalization_layers(self) -> None:
        pass

    def _add_convolutional_layers(
        self,
    ) -> None:
        # Adapted from
        # https://www.tensorflow.org/tutorials/audio/simple_audio
        #
        # self.model.add(layers.Conv2D(32, 3, activation='relu')),
        # self.model.add(layers.Conv2D(64, 3, activation='relu')),
        # self.model.add(layers.MaxPooling2D()),
        self._model.add(tf.keras.layers.Dropout(0.25)),
        self._model.add(tf.keras.layers.Flatten()),
        self._model.add(tf.keras.layers.Dense(128, activation="relu")),
        self._model.add(tf.keras.layers.Dropout(0.5)),
        self._model.add(tf.keras.layers.Dense(len(self.labels)))

    def _compile(self) -> None:
        self._model.compile(
            optimizer=tf.keras.optimizers.Adam(),
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=["accuracy"],
        )

    def _fit(self, epochs: int) -> None:
        history = self._model.fit(
            x=self._spectrogram_data.train_data,
            y=self._spectrogram_data.train_labels,
            # validation_data=self.test_input,
            epochs=epochs,
            callbacks=tf.keras.callbacks.EarlyStopping(verbose=1, patience=2),
        )
        return history

    def _evaluate(self, epochs: int):
        pass

    def save(self, file_path: Path) -> None:
        tf.keras.models.save_model(self._model, file_path)

    def load(self, file_path: Path) -> None:
        pass
