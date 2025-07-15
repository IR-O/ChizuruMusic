# Use image with Python 3.10 + Node.js preinstalled
FROM nikolaik/python-nodejs:python3.10-nodejs18

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    curl \
    wget \
    bash \
    neofetch \
    software-properties-common \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency file and install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U pip wheel
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run the bot
CMD ["python3", "-m", "Chizuru"]
