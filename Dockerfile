# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /code

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libgl1 libxcb1 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /code
USER appuser

# Expose the port Cloud Run expects
EXPOSE 8080

# Run the application with uvicorn
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1