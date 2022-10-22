from typing import Final

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import predict_genre_router

app: Final = FastAPI(
    title="Top-N Music Genre Classifier",
    description="A web app that predicts an audio clip's genre based on a neural network model",
    version="0.1.0",
    contact={
        "url": "https://github.com/fahaddd-git/Top-N-Music-Genre-Classifier",
    },
    docs_url=None,
    redoc_url="/docs",
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
    tags=["predict", "genre"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
