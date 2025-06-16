import asyncio
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.telegram_bot import run_telegram_bot
from .routers import home, upload
from .settings import UPLOADS_PATH


# Directory to store the uploaded media
os.makedirs(UPLOADS_PATH, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Telegram bot task
    asyncio.create_task(run_telegram_bot())

    yield  # App startup complete

    # You can do cleanup here if needed (e.g. shutdown bot)
    # await bot.shutdown() or similar

app = FastAPI(lifespan=lifespan)

# Routers
app.include_router(home.router)
app.include_router(upload.router)

# Directory to store the uploaded media
app.mount(
    "/uploads",
    StaticFiles(directory=UPLOADS_PATH),
    name="uploads"
)
