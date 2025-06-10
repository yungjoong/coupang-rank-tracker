FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    xvfb \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and env files
COPY requirements.txt .env.example ./
RUN cp .env.example .env
RUN pip install -r requirements.txt

# Copy the application code
COPY src/ ./src/

# Set up Xvfb
ENV DISPLAY=:0
RUN echo 'Xvfb :0 -screen 0 1024x768x16 &' > /etc/init.d/xvfb \
    && chmod +x /etc/init.d/xvfb

# Set up entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
