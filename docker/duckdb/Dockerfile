FROM python:3.11-slim

# Install system dependencies (incluindo toolchain para compilar wheels se necessário)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Atualizar pip/setuptools/wheel para evitar erros de build
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Instalar dependências Python
# Obs: aqui NÃO precisamos de boto3 nem s3fs/fsspec, pois o acesso S3 é feito
# via extensão httpfs do próprio DuckDB, não via SDK Python.
RUN pip install --no-cache-dir \
    duckdb==0.10.0 \
    pyarrow==14.0.1 \
    pandas==2.1.3 \
    faker==20.1.0

# Set working directory
WORKDIR /app

# Create directories
RUN mkdir -p /app/scripts /app/data /app/lakehouse

# Default command
CMD ["python"]

