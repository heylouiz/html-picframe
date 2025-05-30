from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, PlainTextResponse
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
    return """
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>Digital Photo Frame</title>
        <script src=\"https://cdn.tailwindcss.com\"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fira+Code&display=swap');
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                background: black;
                font-family: 'Fira Code', monospace;
            }
        </style>
    </head>
    <body class=\"relative flex items-center justify-center overflow-hidden\">
        <div id=\"container\" class=\"w-full h-full flex items-center justify-center\"></div>
        <div id=\"clock\" class=\"absolute top-5 right-8 text-white text-3xl drop-shadow-lg bg-black/50 px-4 py-1 rounded-xl\"></div>
        <div id=\"weather\" class=\"absolute top-5 left-8 text-white text-lg bg-black/40 px-4 py-1 rounded-lg cursor-pointer\">Loading weather...</div>
        <div id=\"forecast\" class=\"absolute bottom-5 left-1/2 transform -translate-x-1/2 text-white text-sm bg-black/50 px-4 py-2 rounded-lg max-w-3xl whitespace-pre-line text-center hidden\"></div>

        <script>
            function updateMedia() {
                fetch('/static/current.meta')
                    .then(res => res.text())
                    .then(ext => {
                        const container = document.getElementById('container');
                        const timestamp = `?cacheBust=${Date.now()}`;
                        const lowerExt = ext.toLowerCase();
                        if (lowerExt === '.jpg' || lowerExt === '.jpeg' || lowerExt === '.png' || lowerExt === '.gif') {
                            container.innerHTML = `<img src='/static/current${ext}${timestamp}' class='max-w-full max-h-full object-contain' />`;
                        } else if (lowerExt === '.mp4') {
                            container.innerHTML = `<video src='/static/current${ext}${timestamp}' autoplay loop muted class='max-w-full max-h-full object-contain'></video>`;
                        } else {
                            container.innerHTML = `<p class='text-white'>Unsupported file type: ${ext}</p>`;
                        }
                    });
            }

            function updateClock() {
                const now = new Date();
                const hours = now.getHours().toString().padStart(2, '0');
                const minutes = now.getMinutes().toString().padStart(2, '0');
                const clock = document.getElementById('clock');
                clock.textContent = `${hours}:${minutes}`;
            }

            async function updateWeather() {
                try {
                    const res = await fetch("/weather");
                    const weatherText = await res.text();
                    document.getElementById("weather").textContent = weatherText;
                } catch (e) {
                    document.getElementById("weather").textContent = "Weather unavailable";
                }
            }

            async function toggleForecast() {
                const forecastDiv = document.getElementById("forecast");
                if (forecastDiv.classList.contains("hidden")) {
                    try {
                        const res = await fetch("/forecast");
                        const text = await res.text();
                        forecastDiv.textContent = text;
                        forecastDiv.classList.remove("hidden");
                    } catch (e) {
                        forecastDiv.textContent = "Forecast unavailable.";
                        forecastDiv.classList.remove("hidden");
                    }
                } else {
                    forecastDiv.classList.add("hidden");
                }
            }

            document.getElementById("weather").addEventListener("click", toggleForecast);

            updateMedia();
            updateClock();
            updateWeather();
            setInterval(updateMedia, 10000);
            setInterval(updateClock, 1000);
            setInterval(updateWeather, 600000); // every 10 minutes
        </script>
    </body>
    </html>
    """

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

