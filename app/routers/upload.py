from fastapi import UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
from pathlib import Path
from fastapi import APIRouter

router = APIRouter()

MEDIA_PATH = "static/current"
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

    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.mp4']:
        media_file_path = MEDIA_PATH + ext
        with open(media_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with open(MEDIA_PATH + ".meta", "w") as metafile:
            metafile.write(ext)

        return {"status": "uploaded", "type": content_type, "filename": filename}
    else:
        return {"error": f"Unsupported file extension: {ext}"}

