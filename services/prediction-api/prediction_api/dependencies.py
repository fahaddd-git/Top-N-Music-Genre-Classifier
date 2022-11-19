import json
from functools import cache

import tensorflow as tf
from prediction_api.config import get_settings

SETTINGS = get_settings()


@cache
def get_model() -> tf.keras.Sequential:
    """Return genre prediction Tensorflow model"""
    model = tf.keras.models.load_model(
        filepath=SETTINGS.model_dir,
        compile=True,
    )
    return model


@cache
def get_label_map() -> dict[int, str]:
    """Return index-to-string label decoder"""
    with open(SETTINGS.labels_json, "r") as labels:
        parsed_json = json.load(labels)
        label_map = {int(index): label for index, label in parsed_json.items()}
        return label_map
