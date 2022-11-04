import io
import os
import random
import string
from functools import cache
from pathlib import Path
from typing import Final

import tensorflow as tf
from fastapi import APIRouter, HTTPException, UploadFile, status
from pydantic import BaseModel
from utilities.audio_processor import convert_sound_to_image

# IANA is the official registry of MIME media types.
# See https://www.iana.org/assignments/media-types/media-types.xhtml and
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
#: Supported "audio/" content subtypes
SUPPORTED_AUDIO_CONTENT_SUBTYPES: Final = frozenset(
    (
        "mpeg",
        "oog",
        "wav",
        "x-wav",
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


def predict(filestream: bytes) -> dict:
    model = load_model()
    labels_to_str = {
        0: "disco",
        1: "country",
        2: "rock",
        3: "pop",
        4: "jazz",
        5: "metal",
        6: "blues",
        7: "reggae",
        8: "classical",
        9: "hiphop",
    }
    random_string = "".join(random.choices(population=string.ascii_letters, k=12))
    temporary_file_path = f"./{random_string}.wav"
    buffer = io.BytesIO(filestream)
    with open(temporary_file_path, "wb") as outfile:
        outfile.write(buffer.getvalue())
    buffer.close()

    image_buffer = io.BytesIO()
    convert_sound_to_image(temporary_file_path).save(image_buffer, format="PNG")
    os.remove(temporary_file_path)
    image_bytes = image_buffer.getvalue()
    decoded_image = tf.io.decode_image(image_bytes)
    tensor = tf.ragged.stack([decoded_image])
    result = model.predict(tensor)[0]
    result = {labels_to_str.get(i): value for i, value in enumerate(result)}
    return {labels_to_str.get(i): value for i, value in enumerate(result)}


@cache
def load_model():
    """Loads model, assumes it's at ./model"""
    model = tf.keras.models.load_model(
        filepath=Path(__file__).resolve().parent / "model",
        compile=True,
    )
    return model
