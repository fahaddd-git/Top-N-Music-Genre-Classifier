import uvicorn
from prediction_api.config import get_settings

if __name__ == "__main__":
    SETTINGS = get_settings()
    uvicorn.run("app:app", host=SETTINGS.host, port=SETTINGS.port, reload=True)
