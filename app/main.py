from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


from fastapi import Depends, FastAPI

from .routers import home, upload

app = FastAPI()

# Routers
app.include_router(home.router)
app.include_router(upload.router)

# Directory to store the uploaded media
app.mount("/static", StaticFiles(directory="static"), name="static")
