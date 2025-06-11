# html-picframe

A website to be used as a digital picture frame — ideal for reusing an old cellphone, TV, Raspberry Pi, etc.

---

## 📦 Installation (Manual)

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
uvicorn main:app --reload
```

---

## 🐳 Run with Docker (Recommended for production)

### Using Docker Compose (from Docker Hub image)

Run:

```bash
docker-compose up -d
```

### Or build and run locally

```bash
docker build -t html-picframe .
docker run -p 8000:8000 -v $(pwd)/uploads:/app/uploads html-picframe
```

---

## 📤 Send images and videos to it

Upload files via `curl`:

```bash
curl -F "file=@photo.jpg" http://localhost:8000/upload
curl -F "file=@video.mp4" http://localhost:8000/upload
```

Supported formats:
- Images: `.jpg`, `.jpeg`, `.png`, `.gif`
- Videos: `.mp4`

---

## ✅ Features

- Fullscreen display of images and videos
- Live weather and forecast overlay
- Digital clock display
- REST API to upload new content
- Auto-refresh media
- Perfect for fullscreen browsers or kiosk mode

---

Happy framing! 🖼️
