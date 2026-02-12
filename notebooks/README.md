# Notebooks - Ambiente de Análise Integrado

Esta pasta contém notebooks Jupyter integrados com o ecossistema do Lakehouse:
- **DuckDB**: Banco de dados analítico
- **MinIO**: Armazenamento S3-compatible
- **dbt**: Transformações de dados

## Como Usar

### 1. Iniciar o Ambiente

Para iniciar o serviço Jupyter junto com todo o ecossistema:

```bash
docker-compose up -d jupyter
```

Ou para iniciar tudo:

```bash
docker-compose up -d
```

### 2. Acessar o Jupyter Lab

Após iniciar o serviço, acesse:

**Jupyter Lab**: http://localhost:8888

O Jupyter Lab será iniciado automaticamente sem senha (apenas para desenvolvimento local).

### 3. Estrutura de Volumes

Os seguintes volumes são montados no container Jupyter:

- `./notebooks` → `/app/notebooks` - Notebooks (esta pasta)
- `./scripts` → `/app/scripts` - Scripts Python do projeto
- `./data` → `/app/data` - Dados brutos
- `./dbt` → `/app/dbt` - Projeto dbt
- `lakehouse_data` → `/app/lakehouse` - Banco DuckDB compartilhado

### 4. Variáveis de Ambiente

O container Jupyter tem acesso às seguintes variáveis de ambiente:

- `MINIO_ENDPOINT`: Endpoint do MinIO (padrão: `minio:9000`)
- `MINIO_ACCESS_KEY`: Chave de acesso (padrão: `admin`)
- `MINIO_SECRET_KEY`: Chave secreta (padrão: `minioadmin123`)
- `MINIO_BUCKET`: Nome do bucket (padrão: `lakehouse`)
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ENDPOINT`, `AWS_REGION`: Configurações S3

### 5. Notebooks Disponíveis

#### `test_duckdb_connection.ipynb`

Notebook de teste que demonstra:
- Conexão com DuckDB
- Configuração do MinIO/S3
- Execução de queries baseadas em `scripts/example_queries.py`
- Visualizações com matplotlib e seaborn
- Verificação de tabelas do dbt

**Queries incluídas:**
1. Receita por Categoria
2. Tendência de Vendas Mensal
3. Top 10 Clientes
4. Verificação de tabelas do dbt
5. Estatísticas Gerais

## Integração com dbt

Os notebooks podem acessar as tabelas criadas pelo dbt. As tabelas seguem o padrão:
- `dim_*`: Dimensões (ex: `dim_clientes`, `dim_produtos`)
- `fct_*`: Fatos (ex: `fct_vendas`)
- `mart_*`: Marts (ex: `mart_vendas_mensal`)

Para garantir que as tabelas do dbt estejam disponíveis, execute:

```bash
docker-compose exec dbt dbt run
```

## Exemplo de Uso no Notebook

```python
import duckdb
import os

# Conectar ao DuckDB compartilhado
db_path = "/app/lakehouse/lakehouse.duckdb"
con = duckdb.connect(db_path)

# Configurar MinIO
minio_endpoint = os.getenv('MINIO_ENDPOINT', 'minio:9000')
con.execute(f"""
    INSTALL httpfs;
    LOAD httpfs;
    SET s3_endpoint='{minio_endpoint}';
    SET s3_access_key_id='{os.getenv('MINIO_ACCESS_KEY')}';
    SET s3_secret_access_key='{os.getenv('MINIO_SECRET_KEY')}';
    SET s3_use_ssl=false;
""")

# Executar query
df = con.execute("SELECT * FROM vendas_iceberg LIMIT 10").fetchdf()
print(df)
```

## Dependências

O container Jupyter já inclui todas as dependências necessárias:
- Jupyter Lab
- DuckDB
- pandas, matplotlib, seaborn
- boto3, s3fs (para MinIO)
- dbt-core, dbt-duckdb

## Troubleshooting

### Jupyter não inicia

Verifique se a porta 8888 está disponível:

```bash
docker-compose logs jupyter
```

### Não consegue conectar ao DuckDB

Certifique-se de que o serviço `init` foi executado para criar o banco de dados:

```bash
docker-compose up init
```

### Tabelas do dbt não aparecem

Execute o dbt para criar as tabelas:

```bash
docker-compose exec dbt dbt run
```

## Próximos Passos

- Criar notebooks para análises específicas
- Integrar com visualizações interativas (Plotly)
- Adicionar notebooks de ETL
- Criar dashboards com os dados

