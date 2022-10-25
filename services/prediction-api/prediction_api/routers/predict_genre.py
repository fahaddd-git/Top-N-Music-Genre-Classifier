from random import random
from typing import Final

from fastapi import APIRouter, HTTPException, UploadFile, status
from pydantic import BaseModel

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
    all_genres = [
        "blues",
        "rap",
        "rock",
        "jazz",
        "hiphop",
        "hip hop",
        "r&b",
        "folk",
        "alternative",
    ]
    result = {genre: random() for genre in all_genres if random() > 0.50}
    return result
