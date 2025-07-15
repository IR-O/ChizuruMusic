FROM nikolaik/python-nodejs:python3.10-nodejs19

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python -m pip install --upgrade pip

# Copy your bot code into the image
COPY . /app/
WORKDIR /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set entrypoint
CMD ["python3", "-m", "Chizuru"]
