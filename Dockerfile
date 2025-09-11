# Docker image definition for Portfolio Analyzer Flask application - builds Python 3.11 container with MySQL dependencies
FROM python:3.11-slim

WORKDIR /app

# Install system deps for building common Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    libssl-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn python-dotenv

# Copy the rest of the app
COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
