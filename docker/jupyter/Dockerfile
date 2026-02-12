FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Atualizar pip/setuptools/wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Instalar dependências Python para Jupyter + DuckDB + MinIO + dbt
RUN pip install --no-cache-dir \
    # Jupyter
    jupyter==1.0.0 \
    jupyterlab==4.0.9 \
    notebook==7.0.6 \
    ipykernel==6.27.1 \
    # DuckDB e extensões
    duckdb==0.10.0 \
    pyarrow==14.0.1 \
    pandas==2.1.3 \
    # MinIO/S3
    boto3==1.34.0 \
    fsspec==2023.12.2 \
    s3fs==2023.12.2 \
    # Iceberg
    pyiceberg[pyarrow,s3fs]==0.6.0 \
    # dbt
    protobuf==4.25.3 \
    dbt-core==1.7.0 \
    dbt-duckdb==1.7.0 \
    # Visualização
    matplotlib==3.8.2 \
    seaborn==0.13.0 \
    plotly==5.18.0 \
    # Utilitários
    faker==20.1.0 \
    requests==2.31.0

# Set working directory
WORKDIR /app

# Create directories
RUN mkdir -p /app/notebooks /app/scripts /app/data /app/lakehouse /app/dbt

# Configurar Jupyter
RUN jupyter notebook --generate-config && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.port = 8888" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.allow_root = True" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = ''" >> ~/.jupyter/jupyter_notebook_config.py

# Expor porta do Jupyter
EXPOSE 8888

# Default command - iniciar Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--notebook-dir=/app/notebooks"]

