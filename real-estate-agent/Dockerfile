# ========================================
# Dockerfile for Real Estate Agent Project
# ========================================

# Use slim python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only necessary files first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Google Cloud SDK (for gsutil)
RUN apt-get update && apt-get install -y curl gnupg && \
    echo "deb http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && apt-get install -y google-cloud-sdk

# Create folders
RUN mkdir -p data/processed faiss

# Download required files from GCS
RUN gsutil cp gs://real-estate-rag-chatbot/data/processed/processed_subset.csv data/processed_subset.csv
RUN gsutil cp gs://real-estate-rag-chatbot/data/processed/faiss/faiss_index_subset.index faiss_index_subset.index

# Copy source code
COPY agents/ ./agents/
COPY retrieval/ ./retrieval/
COPY app.py .
COPY app_frontend.py .
COPY cloudflared/ ./cloudflared/
COPY custom_theme.css .
COPY indexes/ ./indexes/

# Expose FastAPI port
EXPOSE 8080

# Start the application
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:8080"]
