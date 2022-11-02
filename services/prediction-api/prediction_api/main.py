import uvicorn
from config import global_settings

if __name__ == "__main__":
    uvicorn.run("app:app", host=global_settings.host, port=global_settings.port, reload=True)
