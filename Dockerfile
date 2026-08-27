FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas-dev \
    liblapack-dev \
    libx11-6 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Precompiled dlib — never build dlib from source
RUN pip install --no-cache-dir \
    --only-binary=:all: \
    --no-deps \
    dlib-bin==20.0.1

RUN pip install --no-cache-dir \
    --no-deps \
    face-recognition-models==0.3.0

RUN pip install --no-cache-dir \
    --no-deps \
    face-recognition==1.3.0

# Verify the face stack during the IMAGE BUILD,
# so Render fails here instead of endlessly restarting workers.
RUN python -c "import dlib; import face_recognition_models; import face_recognition; print('FACE STACK OK')"
COPY . .

EXPOSE 10000

CMD ["gunicorn", \
     "-w", "1", \
     "--threads", "4", \
     "--worker-tmp-dir", "/dev/shm", \
     "--timeout", "75", \
     "--graceful-timeout", "15", \
     "--max-requests", "300", \
     "--max-requests-jitter", "30", \
     "-b", "0.0.0.0:10000", \
     "app:app"]
