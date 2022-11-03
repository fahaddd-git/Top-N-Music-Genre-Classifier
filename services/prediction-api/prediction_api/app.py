from pathlib import Path
from typing import Final

from fastapi import Depends, FastAPI, staticfiles
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


@app.get("/")
def test_func(settings: dict = Depends(get_settings)):
    if settings.environment is ENVIRONMENT.PRODUCTION:
        print("here")
        static_files_dir = (Path(__file__) / ".." / ".." / settings.static_content_dir).resolve()
        print(static_files_dir)
        app.mount("/", staticfiles.StaticFiles(directory=static_files_dir, html=True))
    else:
        return {"message": "Hello World"}
