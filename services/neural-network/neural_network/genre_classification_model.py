from pathlib import Path
import tensorflow as tf


class GenreClassificationModel:
    def __init__(self):
        pass

    def _add_preprocessing_layers(self) -> None:
        pass

    def _add_normalization_layers(self) -> None:
        pass

    def _add_convolutional_layers(self) -> None:
        pass

    def _compile(self) -> None:
        pass

    def _fit(self) -> None:
        pass

    def _evaluate(self):
        pass

    def save(self, file_path: Path) -> None:
        tf.keras.models.save_model(self._model, file_path)

    def load(self, file_path: Path) -> None:
        pass
