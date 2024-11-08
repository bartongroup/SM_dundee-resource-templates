# Use official Python parent image
FROM python:3.11.5-slim

# Set the working directory to /app
WORKDIR /app

# Copy the Flask application into the container
COPY ./app /app
COPY requirements.txt .

# Install git need to pip install slivka-client from GitHub
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8088 available to the world outside this container
EXPOSE 8088

# Define environment variable defaults (adjust paths as necessary)
ENV APP_SESSIONS_PATH=/data/sessions \
    APP_LOG_PATH=/var/log/myapp \
    APP_DATABASE_PATH=/data/db/session.sqlite \
    SLIVKA_URL=http://localhost:8080/ \
    APP_EXPIRATION_DAYS=7 \
    FLASK_DEBUG=False

# Optional: Define mount points for volumes
VOLUME ["/data/sessions", "/var/log/myapp", "/data/db"]

# Run app.py when the container launches
CMD ["python", "app.py"]
