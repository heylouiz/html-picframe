FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Install system & build dependencies
RUN apk add --no-cache \
    ffmpeg \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev \
    build-base \
    curl

# Copy files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create static dir if it doesn't exist
RUN mkdir -p /app/static

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
