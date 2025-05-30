# html-picframe

A website to be used as a picture frame (old cellphone, tv, etc)

# Install dependencies

`python -m venv .virtualenv`

`source .venv/bin/activate`

`pip install -r requirements.txt`

# Run

`uvicorn app:app --reloa`

# Send images and videos to it

`curl -F "file=@video.mp4" http://localhost:8000/upload`

`curl -F "file=@photo.jpg" http://localhost:8000/upload`
