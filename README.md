# Modern Lakehouse: DuckDB + Apache Iceberg + MinIO + dbt

Laboratório prático de um **Lakehouse moderno** totalmente containerizado, demonstrando conceitos avançados de engenharia de dados como versionamento, time travel, schema evolution e transformações com dbt.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Conceitos](#conceitos)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Uso](#instalação-e-uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Acessando os Serviços](#acessando-os-serviços)
- [Exemplos de Uso](#exemplos-de-uso)
- [Comparação com Databricks](#comparação-com-databricks)

## 🎯 Visão Geral

Este projeto implementa um **Lakehouse** completo em ambiente local usando:

- **DuckDB**: Engine analítico in-memory otimizado para OLAP
- **Apache Iceberg**: Tabela format para versionamento e time travel
- **MinIO**: Storage S3-compatible para simular cloud storage
- **dbt**: Ferramenta de transformação de dados (ELT)
- **Docker Compose**: Orquestração de todos os serviços

### O que é um Lakehouse?

Um **Lakehouse** combina as melhores características de um **Data Lake** (armazenamento barato, formatos abertos) com as de um **Data Warehouse** (ACID transactions, schema enforcement, performance).

**Vantagens:**
- ✅ Armazenamento econômico (formato Parquet/Delta/Iceberg)
- ✅ Suporte a dados estruturados, semi-estruturados e não estruturados
- ✅ ACID transactions e versionamento
- ✅ Time travel (acessar versões anteriores dos dados)
- ✅ Schema evolution (evoluir schema sem quebrar compatibilidade)
- ✅ Performance de queries analíticas
- ✅ Integração com ferramentas modernas (Spark, dbt, etc)

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         Docker Compose                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │    MinIO     │      │    DuckDB    │      │     dbt      │  │
│  │  (S3 Local)  │◄─────┤  (Analytics) │◄─────┤ (Transform)  │  │
│  │  Port: 9000  │      │              │      │              │  │
│  │  Port: 9001  │      │              │      │              │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│         ▲                    ▲                                   │
│         │                    │                                   │
│         └────────────────────┘                                   │
│              Iceberg Tables                                       │
│         (s3://lakehouse/iceberg/)                                │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Init Service (One-time)                     │   │
│  │  • Cria bucket                                           │   │
│  │  • Gera dados fake                                       │   │
│  │  • Cria tabela Iceberg                                   │   │
│  │  • Insere dados                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Fluxo de Dados

1. **Inicialização**: O serviço `init` cria o bucket no MinIO, gera dados fake e cria a tabela Iceberg
2. **Armazenamento**: Dados são armazenados no MinIO (S3-compatible) em formato Iceberg
3. **Análise**: DuckDB consulta diretamente as tabelas Iceberg no MinIO
4. **Transformação**: dbt transforma os dados brutos em modelos analíticos (marts)

## 📚 Conceitos

### Apache Iceberg

**Apache Iceberg** é uma especificação de tabela aberta para analytics em data lakes. Ele fornece:

- **ACID Transactions**: Garante consistência dos dados
- **Time Travel**: Acesse versões anteriores dos dados
- **Schema Evolution**: Adicione/remova colunas sem quebrar queries antigas
- **Hidden Partitioning**: Particionamento automático e otimizado
- **Metadata Management**: Metadados versionados e eficientes

**Exemplo de Time Travel:**
```sql
-- Ver dados de 1 hora atrás
SELECT * FROM vendas_iceberg 
FOR TIMESTAMP AS OF '2024-01-01 10:00:00';

-- Ver snapshot específico
SELECT * FROM vendas_iceberg 
FOR VERSION AS OF 5;
```

**Exemplo de Schema Evolution:**
```sql
-- Adicionar nova coluna sem quebrar queries antigas
ALTER TABLE vendas_iceberg 
ADD COLUMN novo_campo VARCHAR;
```

### DuckDB

**DuckDB** é um banco de dados analítico in-memory otimizado para OLAP (Online Analytical Processing). Características:

- ⚡ Performance excepcional para queries analíticas
- 🔌 Integração nativa com Parquet, CSV, JSON
- 📦 Extensões para S3, Iceberg, Postgres, etc
- 🐍 Integração Python/R fácil
- 💾 Zero configuração

### MinIO

**MinIO** é um servidor de armazenamento de objetos S3-compatible. Usado aqui para simular cloud storage localmente.

## 🚀 Pré-requisitos

- **Docker** (versão 20.10+)
- **Docker Compose** (versão 2.0+)
- **Git** (para clonar o repositório)

## 📦 Instalação e Uso

### 1. Clone o repositório

```bash
git clone <repo-url>
cd modern-lakehouse-duckdb-iceberg
```

### 2. Inicie os serviços

```bash
docker compose up -d
```

Este comando irá:
- ✅ Baixar as imagens necessárias
- ✅ Criar os containers
- ✅ Configurar volumes persistentes
- ✅ Executar o serviço de inicialização automaticamente

### 3. Verifique os logs

```bash
# Ver logs de todos os serviços
docker compose logs -f

# Ver logs de um serviço específico
docker compose logs -f init
```

### 4. Aguarde a inicialização

O serviço `init` irá:
1. Aguardar MinIO estar disponível
2. Criar o bucket `lakehouse`
3. Gerar 5.000 registros de vendas fake
4. Criar tabela Iceberg `vendas_iceberg`
5. Inserir os dados na tabela

**Tempo estimado**: 1-2 minutos

## 📁 Estrutura do Projeto

```
modern-lakehouse-duckdb-iceberg/
├── docker/
│   ├── duckdb/
│   │   └── Dockerfile          # Imagem DuckDB + Python
│   ├── dbt/
│   │   └── Dockerfile          # Imagem dbt + DuckDB adapter
│   └── init/
│       └── Dockerfile          # Imagem de inicialização
├── dbt/
│   ├── models/
│   │   ├── staging/            # Modelos de staging (limpeza)
│   │   │   ├── stg_vendas.sql
│   │   │   └── schema.yml
│   │   └── marts/              # Modelos analíticos
│   │       ├── fct_vendas.sql
│   │       ├── dim_produtos.sql
│   │       ├── dim_clientes.sql
│   │       ├── mart_vendas_mensal.sql
│   │       └── schema.yml
│   ├── dbt_project.yml         # Configuração do projeto
│   └── profiles.yml            # Perfil de conexão
├── scripts/
│   ├── generate_fake_data.py   # Gera dados fake
│   ├── create_iceberg_table.py # Cria tabela Iceberg
│   ├── example_queries.py      # Queries de exemplo
│   └── init_lakehouse.py       # Script de inicialização
├── data/                       # Dados gerados (volumes)
├── docker-compose.yml          # Orquestração dos serviços
└── README.md                   # Este arquivo
```

## ⚙️ Funcionalidades

### ✅ Funcionalidades Implementadas

1. **Criação Automática de Bucket**
   - Bucket `lakehouse` criado automaticamente no MinIO

2. **Geração de Dados Fake**
   - 5.000 registros de vendas simulados
   - Dados realistas com produtos, clientes, descontos, etc

3. **Tabela Iceberg**
   - Tabela `vendas_iceberg` com particionamento por ano/mês
   - Armazenada no MinIO em formato Iceberg

4. **Queries Analíticas**
   - 8 queries de exemplo demonstrando análises de negócio
   - Time travel e schema evolution

5. **Transformações dbt**
   - Modelos staging (limpeza)
   - Modelos marts (análise)
   - Dimensões e fatos

## 🌐 Acessando os Serviços

### MinIO Console

**URL**: http://localhost:9001

**Credenciais**:
- Usuário: `admin`
- Senha: `minioadmin123`

No console você pode:
- Ver buckets e objetos
- Navegar pela estrutura de arquivos Iceberg
- Ver metadados

### DuckDB (via container)

```bash
# Entrar no container DuckDB
docker compose exec duckdb bash

# Executar Python interativo
python

# Ou executar scripts diretamente
docker compose exec duckdb python /app/scripts/example_queries.py
```

### dbt

```bash
# Entrar no container dbt
docker compose exec dbt bash

# Executar modelos
dbt run

# Executar testes
dbt test

# Gerar documentação
dbt docs generate
dbt docs serve --port 8080
```

## 💡 Exemplos de Uso

### 1. Executar Queries de Exemplo

```bash
docker compose exec duckdb python /app/scripts/example_queries.py
```

Isso executará 8 queries demonstrando:
- Receita por categoria
- Tendência de vendas mensal
- Top clientes
- Análise por canal
- Time travel
- Schema evolution
- Performance de produtos
- Análise regional

### 2. Executar Transformações dbt

```bash
# Executar todos os modelos
docker compose exec dbt dbt run

# Executar apenas staging
docker compose exec dbt dbt run --select staging

# Executar apenas marts
docker compose exec dbt dbt run --select marts

# Executar testes
docker compose exec dbt dbt test
```

### 3. Query Direta no DuckDB

```bash
docker compose exec duckdb python
```

```python
import duckdb
import os

# Conectar
con = duckdb.connect()

# Configurar S3
con.execute("""
    INSTALL httpfs;
    LOAD httpfs;
    SET s3_endpoint='minio:9000';
    SET s3_access_key_id='admin';
    SET s3_secret_access_key='minioadmin123';
    SET s3_use_ssl=false;
    SET s3_url_style='path';
""")

# Query
result = con.execute("""
    SELECT 
        categoria,
        COUNT(*) as total,
        SUM(valor_final) as receita
    FROM vendas_iceberg
    GROUP BY categoria
    ORDER BY receita DESC;
""").fetchdf()

print(result)
```

### 4. Adicionar Mais Dados

```bash
# Gerar mais dados
docker compose exec duckdb python /app/scripts/generate_fake_data.py

# Inserir na tabela Iceberg
docker compose exec duckdb python -c "
import sys
sys.path.append('/app/scripts')
from create_iceberg_table import *
con = duckdb.connect()
setup_s3_connection(con)
insert_data_from_parquet(con, '/app/data/vendas_raw.parquet')
"
```

### 5. Explorar Metadados Iceberg

```bash
# Listar snapshots (via MinIO Console ou código)
docker compose exec duckdb python -c "
import duckdb
con = duckdb.connect()
# Configurar S3...
# Consultar metadados Iceberg
"
```

## 🔄 Comparação com Databricks

Este projeto simula uma arquitetura similar ao **Databricks Lakehouse**:

| Recurso | Databricks | Este Projeto |
|---------|-----------|--------------|
| **Storage** | DBFS / S3 / ADLS | MinIO (S3-compatible) |
| **Table Format** | Delta Lake | Apache Iceberg |
| **Query Engine** | Spark SQL | DuckDB |
| **Transform** | dbt / Spark | dbt |
| **Time Travel** | ✅ Sim | ✅ Sim (Iceberg) |
| **Schema Evolution** | ✅ Sim | ✅ Sim (Iceberg) |
| **ACID** | ✅ Sim | ✅ Sim (Iceberg) |
| **UI** | Databricks Notebooks | Docker CLI / MinIO Console |

### Vantagens deste Projeto

- ✅ **100% Local**: Roda completamente offline
- ✅ **Zero Custo**: Sem necessidade de cloud
- ✅ **Educacional**: Ideal para aprender conceitos
- ✅ **Rápido Setup**: `docker compose up` e pronto
- ✅ **Open Source**: Todas as tecnologias são open source

### Limitações vs Databricks

- ⚠️ **Escala**: Limitado a máquina local (vs cluster distribuído)
- ⚠️ **Colaboração**: Sem notebooks compartilhados
- ⚠️ **ML**: Sem MLflow integrado
- ⚠️ **Governança**: Sem Unity Catalog
- ⚠️ **Performance**: DuckDB é single-node (vs Spark distribuído)

## 🛠️ Troubleshooting

### MinIO não inicia

```bash
# Verificar logs
docker compose logs minio

# Reiniciar serviço
docker compose restart minio
```

### Tabela Iceberg não encontrada

```bash
# Re-executar inicialização
docker compose up init
```

### Erro de conexão S3

Verifique as variáveis de ambiente no `docker-compose.yml` e certifique-se de que o MinIO está rodando.

### dbt não encontra tabela

Certifique-se de que a tabela Iceberg foi criada primeiro:
```bash
docker compose exec duckdb python /app/scripts/create_iceberg_table.py
```

## 📝 Próximos Passos

Ideias para expandir o projeto:

- [ ] Adicionar mais tabelas (clientes, produtos separados)
- [ ] Implementar streaming de dados
- [ ] Adicionar testes automatizados
- [ ] Criar dashboards (Grafana/Metabase)
- [ ] Implementar CI/CD
- [ ] Adicionar Airflow para orquestração
- [ ] Implementar data quality checks

## 📄 Licença

Este projeto é open source e está disponível para fins educacionais.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📚 Referências

- [Apache Iceberg](https://iceberg.apache.org/)
- [DuckDB](https://duckdb.org/)
- [MinIO](https://min.io/)
- [dbt](https://www.getdbt.com/)
- [Databricks Lakehouse](https://www.databricks.com/product/data-lakehouse)

---

**Desenvolvido com ❤️ para aprendizado de engenharia de dados modernos**
