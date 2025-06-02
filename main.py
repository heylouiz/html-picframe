from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from pathlib import Path
import httpx

app = FastAPI()

# Directory to store the uploaded media
MEDIA_PATH = "static/current"
os.makedirs("static", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def get_frame():
    return FileResponse("index.html")

@app.get("/up", response_class=HTMLResponse)
async def upload_form():
    return FileResponse("up.html")

@app.get("/weather", response_class=PlainTextResponse)
async def proxy_weather():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://wttr.in/?format=%t+%C")
        return r.text

@app.get("/forecast", response_class=PlainTextResponse)
async def proxy_forecast():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://wttr.in?format=%l:+%c+%t+%wNLNLForecast:NL%f")
        return r.text.replace("NL", "\n")

@app.post("/upload")
async def upload_media(file: UploadFile = File(...)):
    content_type = file.content_type.lower()
    print(f"Uploaded content type: {content_type}")

    filename = file.filename.lower()
    ext = Path(filename).suffix

    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.mp4']:
        media_file_path = MEDIA_PATH + ext
        with open(media_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with open(MEDIA_PATH + ".meta", "w") as metafile:
            metafile.write(ext)

        return {"status": "uploaded", "type": content_type, "filename": filename}
    else:
        return {"error": f"Unsupported file extension: {ext}"}

