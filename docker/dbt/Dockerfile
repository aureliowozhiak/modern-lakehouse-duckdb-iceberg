FROM python:3.11-slim

# Install system dependencies (incluindo toolchain para eventuais compilações)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Atualizar pip/setuptools/wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install dbt and DuckDB adapter
# Obs: o dbt-duckdb usa extensões nativas do DuckDB (httpfs/iceberg),
# não precisamos de s3fs/boto3 aqui.
# Fix protobuf version to avoid compatibility issues with dbt-core 1.7.0
# Using specific version 4.25.3 (last 4.x version) to avoid shell redirection issues
RUN pip install --no-cache-dir \
    protobuf==4.25.3 \
    dbt-core==1.7.0 \
    dbt-duckdb==1.7.0 \
    duckdb==0.10.0 \
    pyarrow==14.0.1

# Set working directory
WORKDIR /dbt

# Default command
CMD ["dbt", "--version"]

