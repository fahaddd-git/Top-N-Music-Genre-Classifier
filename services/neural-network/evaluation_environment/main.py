import io
from functools import cache
from pathlib import Path
from pprint import pprint

import tensorflow as tf
from keras.models import Sequential
from neural_network.data_ingestion_helpers import _get_genre_labels
from utilities.audio_processor import convert_sound_to_image

"""
A script to make evaluating the model easier. Some of the logic is duplicated from other places in
the codebase. To be resolved once API endpoints are in place
"""


def load_model() -> Sequential:
    """Loads model, assumes it's at ./model"""
    model = tf.keras.models.load_model(
        filepath=Path(__file__).resolve().parent / "model",
        compile=True,
    )
    return model


def get_sound_file_as_ragged_tensor(path: str) -> tf.RaggedTensor:
    # PIL requires a buffer to write properly-formatted PNG data...
    image_buffer = io.BytesIO()
    convert_sound_to_image(path).save(image_buffer, format="PNG")
    # ... but TF needs raw bytes from the stream to load the image
    image_bytes = image_buffer.getvalue()
    decoded_image = tf.io.decode_image(image_bytes)
    tensor = tf.ragged.stack([decoded_image])
    return tensor


def predict(model: Sequential, path: str):
    tensor = get_sound_file_as_ragged_tensor(path)
    return to_genres(model.predict(tensor)[0])  # should only be one element in the top tensor


def to_genres(result_list: list[float]) -> dict[str, float]:
    """Temporary for demo"""
    # cache so we only access database once, then immediately run the cached function
    labels_to_str = cache(lambda: {key - 1: val for key, val in _get_genre_labels().items()})()
    return {labels_to_str.get(i): value for i, value in enumerate(result_list)}


def main():
    print("Loading model...")
    model = load_model()
    print("Successfully loaded model")

    while True:
        print("")
        path = input("Enter a file path to a 30-second .wav clip:\n")
        while not Path(path).resolve().exists():
            print("Invalid path. Try again.")
            path = input("Enter a file path to a 30-second .wav clip:\n")

        prediction = predict(model, path)
        best_guess = max(prediction.items(), key=lambda key_value_pair: key_value_pair[1])
        genre, confidence = best_guess
        print("")
        print(f"Best genre guess was {genre} with a confidence of {confidence:.2%}")
        print("Full prediction results:")
        pprint({key: f"{val:.2%}" for key, val in prediction.items()})

        try_again = input("Try again (y/n)? ").strip().lower()
        if try_again == "n":
            raise SystemExit


if __name__ == "__main__":
    main()
