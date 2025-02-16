FROM python:3.12-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download and install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin:$PATH"

# Set up the application directory
WORKDIR /app

# Copy requirements.txt first (for caching layers)
COPY requirements.txt /app/requirements.txt

# Install Python dependencies properly
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Expose Flask API port (if required)
EXPOSE 8000

# Set environment variables for Flask & FastAPI
ENV FLASK_APP=tasksB.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

# Start FastAPI (change if Flask should run instead)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
