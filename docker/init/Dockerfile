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
# Obs: aqui precisamos de boto3 (para criar bucket) e pyiceberg para criar tabelas Iceberg reais
RUN pip install --no-cache-dir \
    duckdb==0.10.0 \
    pyarrow==14.0.1 \
    pandas==2.1.3 \
    faker==20.1.0 \
    boto3==1.34.0 \
    fsspec==2023.12.2 \
    s3fs==2023.12.2 \
    pyiceberg[pyarrow,s3fs]==0.6.0 \
    requests==2.31.0

# Set working directory
WORKDIR /app

# Create directories
RUN mkdir -p /app/scripts /app/data /app/lakehouse

# Default command
CMD ["python"]

