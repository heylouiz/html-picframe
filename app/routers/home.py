from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import httpx

router = APIRouter()

# Directory to store the uploaded media
MEDIA_PATH = "static/current"
os.makedirs("static", exist_ok=True)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_frame(request: Request):
    # Read media extension
    try:
        with open(f"{MEDIA_PATH}.meta", "r") as f:
            media_ext = f.read().strip()
    except FileNotFoundError:
        media_ext = None

    media_tag = ""
    if media_ext:
        if media_ext in ['.jpg', '.jpeg', '.png', '.gif']:
            media_tag = f"<img src='/static/current{media_ext}' class='max-w-full max-h-full object-contain' />"
        elif media_ext == '.mp4':
            media_tag = f"<video src='/static/current{media_ext}' autoplay loop muted class='max-w-full max-h-full object-contain'></video>"
        else:
            media_tag = f"<p class='text-white'>Unsupported file type: {media_ext}</p>"
    else:
        media_tag = "<p class='text-white text-lg'>No media uploaded yet.</p>"

    # Get weather string
    try:
        async with httpx.AsyncClient() as client:
            weather_response = await client.get("https://wttr.in/?format=%t+%C")
            weather = weather_response.text.strip()
    except Exception:
        weather = "Weather unavailable"

    # Get forecast string
    try:
        async with httpx.AsyncClient() as client:
            forecast_response = await client.get("https://wttr.in?format=%l:+%c+%t+%w\n\nForecast:\n%f")
            print(forecast_response)
            forecast = forecast_response.text.strip()
    except Exception:
        forecast = "Forecast unavailable"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "media_tag": media_tag,
        "weather": weather,
        "forecast": forecast
    })
