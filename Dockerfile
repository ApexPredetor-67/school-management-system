FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas-dev \
    liblapack-dev \
    libx11-6 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Install normal Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Install PRECOMPILED dlib wheel only.
# --only-binary prevents pip from attempting a source build.
RUN pip install --no-cache-dir \
    --only-binary=:all: \
    --no-deps \
    dlib-bin==20.0.1

# face-recognition is installed without dependencies because
# dlib-bin supplies the dlib module.
RUN pip install --no-cache-dir \
    --no-deps \
    face-recognition==1.3.0

COPY . .

EXPOSE 10000

CMD ["gunicorn", \
     "-w", "1", \
     "--threads", "4", \
     "--worker-tmp-dir", "/dev/shm", \
     "-b", "0.0.0.0:10000", \
     "--timeout", "75", \
     "--graceful-timeout", "15", \
     "--max-requests", "300", \
     "--max-requests-jitter", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "app:app"]
