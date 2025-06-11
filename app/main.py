import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import home, upload
from .settings import UPLOADS_PATH


# Directory to store the uploaded media
os.makedirs(UPLOADS_PATH, exist_ok=True)

app = FastAPI()

# Routers
app.include_router(home.router)
app.include_router(upload.router)

# Directory to store the uploaded media
app.mount(
    "/uploads",
    StaticFiles(directory=UPLOADS_PATH),
    name="uploads"
)
