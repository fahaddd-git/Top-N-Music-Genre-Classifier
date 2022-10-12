from fastapi import FastAPI, UploadFile
import os

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello World" }

@app.post("/upload")
async def upload_file(file: UploadFile):
    # return { "fileSize": os.stat(file.filename).st_size }
    return { "foo": file.filename }
