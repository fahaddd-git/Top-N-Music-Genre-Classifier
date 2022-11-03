from pathlib import Path
from typing import Final

from fastapi import FastAPI, staticfiles
from fastapi.middleware.cors import CORSMiddleware
from prediction_api.config import ENVIRONMENT, get_settings
from prediction_api.routers.predict_genre import router as predict_genre_router

app: Final = FastAPI(
    title="Top-N Music Genre Classifier",
    description="A web app that predicts an audio clip's genre based on a neural network model",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    predict_genre_router,
    prefix="/api/predict-genres",
    tags=["predict-genre"],
)

if get_settings().environment is ENVIRONMENT.PRODUCTION:
    static_files_dir = (Path(__file__) / ".." / ".." / get_settings().static_content_dir).resolve()
    app.mount("/", staticfiles.StaticFiles(directory=static_files_dir, html=True))
else:

    @app.get("/")
    async def root():
        return {"message": "Hello World"}
