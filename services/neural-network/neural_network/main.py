import io
from pathlib import Path

import tensorflow as tf
from genre_classification_model import GenreClassificationModel
from neural_network.data_ingestion_helpers import train_test_split
from utilities.audio_processor import convert_sound_to_image


def create_and_fit_model(epochs: int):
    spectrogram_data = train_test_split()
    model = GenreClassificationModel(spectrogram_data)
    model.fit(epochs)
    return model


def evaluate_and_save_model(model: GenreClassificationModel):
    results = model.evaluate()
    print("")
    print("Results")
    print(f"Loss:\t{results.get('loss')}")
    print(f"Accuracy:\t{results.get('accuracy')}")
    print("")
    should_save = input("Save model (y/n)? ").strip().lower()
    if should_save == "y":
        print("Saving to '~/model/'...")
        model.save(Path.home() / "model")
        print("Success")
        print("")


def predict(model: GenreClassificationModel, path: str):
    # PIL requires a buffer to write properly-formatted PNG data...
    image_buffer = io.BytesIO()
    convert_sound_to_image(path).save(image_buffer, format="PNG")
    # ... but TF needs raw bytes from the stream to load the image
    image_bytes = image_buffer.getvalue()
    decoded_image = tf.io.decode_image(image_bytes)
    tensor = tf.ragged.stack([decoded_image])
    return to_genres(model.predict(tensor)[0])  # should only be one element in the top tensor


def to_genres(result_list: list[float]) -> dict[str, float]:
    """Temporary for demo"""
    from functools import cache

    from data_ingestion_helpers import _get_genre_labels

    # cache so we only access database once, then immediately run the cached function
    labels_to_str = cache(lambda: {key - 1: val for key, val in _get_genre_labels().items()})()
    return {labels_to_str.get(i): value for i, value in enumerate(result_list)}


if __name__ == "__main__":
    while True:
        num_epochs = 10
        spectrogram_model = create_and_fit_model(num_epochs)
        results = predict(spectrogram_model, "./clips/mozart.wav")
        print("-----\nMozart:")
        print(results, sep="\n")
        print("-----")
        evaluate_and_save_model(spectrogram_model)
        try_again = input("Try again (y/n)? ").strip().lower()
        if try_again == "n":
            raise SystemExit
