from pathlib import Path

from ..settings import UPLOADS_PATH


ALLOWED_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".mp4"
)

META_PATH = Path(UPLOADS_PATH) / ".meta"


def get_current_media_path():
    with open(META_PATH, "r") as f:
        return f.read().strip()


def set_current_media_path(filename: str):
    with open(META_PATH, "w") as f:
        return f.write(str(filename))

