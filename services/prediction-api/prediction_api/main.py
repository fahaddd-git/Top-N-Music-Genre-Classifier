import uvicorn
from prediction_api.config import get_settings

SETTINGS = get_settings()


def start_server():
    uvicorn.run(
        "prediction_api.app:app",
        host=SETTINGS.host,
        port=SETTINGS.port,
        reload=SETTINGS.debug,
    )


if __name__ == "__main__":
    start_server()
