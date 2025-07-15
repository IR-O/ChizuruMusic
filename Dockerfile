FROM python:3.10.4-slim-buster

# Install Node.js 18.x, FFmpeg, and essential packages
RUN apt update && apt upgrade -y && \
    apt install -y curl gnupg ffmpeg git wget bash neofetch software-properties-common && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verify essential versions (optional)
RUN node -v && npm -v && ffmpeg -version && python3 --version

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U pip wheel
RUN pip3 install --no-cache-dir -r requirements.txt

# Set working directory
WORKDIR /app
COPY . .

# Run the bot
CMD ["python3", "-m", "Chizuru"]
