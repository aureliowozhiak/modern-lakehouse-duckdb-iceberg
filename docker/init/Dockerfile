FROM python:3.11-slim

# Install system dependencies (incluindo toolchain de build, se necessário)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Atualizar pip/setuptools/wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies
# Obs: aqui precisamos de boto3 (para criar bucket), mas NÃO de s3fs/fsspec.
RUN pip install --no-cache-dir \
    duckdb==0.10.0 \
    pyarrow==14.0.1 \
    pandas==2.1.3 \
    faker==20.1.0 \
    boto3==1.29.7 \
    requests==2.31.0

# Set working directory
WORKDIR /app

# Create directories
RUN mkdir -p /app/scripts /app/lakehouse

# Default command
CMD ["python"]

