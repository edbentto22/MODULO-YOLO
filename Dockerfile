# Backend FastAPI for MODULO-YOLO
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Create non-root user for security
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app.py ./
# index.html is not served by the backend, but copy is harmless if needed later
COPY index.html ./

# Ensure uploads directory exists and is writable
RUN mkdir -p /app/imagens && chown -R appuser:appuser /app/imagens

ENV PORT=8000
EXPOSE 8000

USER appuser

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]