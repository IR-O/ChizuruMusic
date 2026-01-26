FROM python:3.10-bullseye

# Install system deps
RUN apt-get update && \
    apt-get install -y \
        ffmpeg \
        git \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 18.x (for PyTgCalls)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get update && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "-m", "Chizuru"]
