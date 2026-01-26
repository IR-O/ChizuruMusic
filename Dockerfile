FROM python:3.10-bullseye

# Install system deps + nodejs
RUN apt-get update && \
    apt-get install -y \
        ffmpeg \
        git \
        nodejs \
        npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "-m", "Chizuru"]
