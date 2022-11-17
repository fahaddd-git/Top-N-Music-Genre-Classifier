import io
import json
from functools import cache
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Final

import numpy as np
import tensorflow as tf
from fastapi import APIRouter, HTTPException, UploadFile, status
from pydantic import BaseModel
from utilities.audio_processor import generate_sound_images

# IANA is the official registry of MIME media types.
# See https://www.iana.org/assignments/media-types/media-types.xhtml and
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
#: Supported "audio/" content subtypes
SUPPORTED_AUDIO_CONTENT_SUBTYPES: Final = frozenset(
    (
        "mpeg",
        "wav",
        "x-wav",
        "flac",
        "x-flac",
    )
)

router: Final = APIRouter()


class GenrePredictionResponse(BaseModel):
    """Response model for the genre prediction endpoint"""

    # Dynamic key-value pairs: https://pydantic-docs.helpmanual.io/usage/models/#custom-root-types
    __root__: dict[str, float]

    class Config:
        schema_extra = {
            # OpenAPI schema examples for FastAPI spec generator
            "example": {
                "classical": 0.86,
                "folk": 0.14,
            }
        }


@router.post("/", response_model=GenrePredictionResponse)
async def predict_genre(file: UploadFile):
    if not is_supported_audio_file(file):
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Unsupported content type {file.content_type}",
        )
    filestream = await file.read()
    return predict(filestream)


def is_supported_audio_file(file: UploadFile) -> bool:
    """Return whether the passed file represents a supported audio file"""
    mime_type, _, mime_subtype = file.content_type.partition("/")
    mime_subtype = mime_subtype.split(";")[0]  # discard optional mime parameters
    return mime_type == "audio" and mime_subtype in SUPPORTED_AUDIO_CONTENT_SUBTYPES


def predict(sound_data: bytes) -> dict[str, float]:
    """Predict the genre corresponding to the passed sound data

    :param sound_data: bytes read from a supported audio file
    :return: dict of genre-confidence pairs
    """
    model = get_model()
    label_map = get_label_mappings()

    input_tensor = construct_input_tensor(sound_data)
    probabilities = model.predict(input_tensor)
    flattened_probabilities = np.mean(probabilities, axis=0)

    result = {
        label_map.get(i, f"Genre {i}"): value for i, value in enumerate(flattened_probabilities)
    }
    return result


def construct_input_tensor(sound_data: bytes) -> tf.RaggedTensor:
    """Construct an input tensor from the passed sound file data

    :param sound_data: bytes read from a supported audio file
    :return: a stacked ragged tensor
    """
    images = []
    with NamedTemporaryFile() as sound_file:
        sound_file.write(sound_data)
        for image in generate_sound_images(
            sound_file.name,
            desired_segments_seconds=30,
            duration=90,
        ):
            with io.BytesIO() as image_buffer:
                image.save(image_buffer, format="PNG")
                image_bytes = image_buffer.getvalue()
                decoded_image = tf.io.decode_image(image_bytes)
                images.append(decoded_image)
    tensor = tf.ragged.stack(images)
    return tensor


@cache
def get_model():
    """Loads model, assumes it's at ./model"""
    model = tf.keras.models.load_model(
        filepath=Path(__file__).resolve().parent / "model",
        compile=True,
    )
    return model


@cache
def get_label_mappings():
    """Loads numeric-to-string label decoder, assumes it's at ./model"""
    labels_json = Path(__file__).resolve().parent / "model" / "labels.json"
    with open(labels_json, "r") as labels:
        parsed_json = json.load(labels)
        label_mapper = {int(index): label for index, label in parsed_json.items()}
        return label_mapper
