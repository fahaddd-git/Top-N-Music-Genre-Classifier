from typing import List
from fastapi import FastAPI, UploadFile, HTTPException, status
from prediction_api.mock_prediction import predict
from prediction_api.config import content_type_audio

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


async def _handle_audio_file(file: UploadFile) -> dict:
    if file.content_type not in content_type_audio:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"{file.filename}: {file.content_type} not in {content_type_audio}"
        )
    return predict(await file.read())


@app.post("/uploadfile")
async def upload_file(file: UploadFile):
    return await _handle_audio_file(file)


@app.post("/uploadfiles")
async def upload_files(files: List[UploadFile]) -> dict:
    predictions = {}
    for file in files:
        predictions[file.filename] = await _handle_audio_file(file)
    return predictions
