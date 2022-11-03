from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prediction_api.config import get_settings
from prediction_api.routers.predict_genre import router as predict_genre_router

SETTINGS = get_settings()

app = FastAPI(
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

# resolve static content server
static_content_dir = Path(__file__).resolve().parent / SETTINGS.static_content_dir
static_content_app = StaticFiles(
    directory=static_content_dir,
    html=True,
    check_dir=False,
)
if Path(static_content_dir).is_dir():
    app.mount("/", app=static_content_app, name="static")
