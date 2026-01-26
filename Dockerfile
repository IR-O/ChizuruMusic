FROM python:3.10-bullseye

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        ffmpeg \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy project
COPY . /app

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Start bot
CMD ["python3", "-m", "Chizuru"]
