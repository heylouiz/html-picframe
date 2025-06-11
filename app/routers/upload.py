from fastapi import UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
from pathlib import Path
from fastapi import APIRouter

from ..settings import UPLOAD_FILENAME, UPLOADS_PATH
from ..utils.misc import ALLOWED_EXTENSIONS, set_current_media_path

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/up", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("up.html", {
        "request": request,
    })

@router.post("/upload")
async def upload_media(file: UploadFile = File(...)):
    content_type = file.content_type.lower()
    print(f"Uploaded content type: {content_type}")

    filename = file.filename.lower()
    ext = Path(filename).suffix

    if ext in ALLOWED_EXTENSIONS:
        media_filename = f"{UPLOAD_FILENAME}{ext}"
        media_file_path = Path(UPLOADS_PATH) / media_filename
        with open(media_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        set_current_media_path(media_file_path)

        return {"status": "uploaded", "type": content_type, "filename": filename}
    else:
        return {"error": f"Unsupported file extension: {ext}"}

