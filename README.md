# Modern Opensource Lakehouse: DuckDB + Apache Iceberg + MinIO + dbt

Laboratório prático de um **Lakehouse moderno e 100% open source** totalmente containerizado, demonstrando conceitos avançados de engenharia de dados como versionamento, time travel, schema evolution e transformações com dbt.


> 🚀 **Reproduza um Lakehouse moderno, feature-complete e open source em minutos usando DuckDB, Iceberg, MinIO e dbt – tudo orquestrado via Docker Compose.**
>
> - **Time travel**, **schema evolution** e **tables versionadas**
> - Transforma dados usando **dbt** (Python)
> - Exemplo 100% prático + scripts didáticos
> - **Notebooks Jupyter** prontos para análise
> - Deploy local, 100% open (sem cloud/lock-in!)

[![Repositório no GitHub](https://img.shields.io/github/stars/aureliowozhiak/modern-lakehouse-duckdb-iceberg?style=social)](https://github.com/aureliowozhiak/modern-lakehouse-duckdb-iceberg)

---

- **Repositório:** [https://github.com/aureliowozhiak/modern-lakehouse-duckdb-iceberg](https://github.com/aureliowozhiak/modern-lakehouse-duckdb-iceberg)
- **Documentação completa:** Veja exemplos de queries, screenshots, vídeos e detalhes técnicos no [repositório do GitHub](https://github.com/aureliowozhiak/modern-lakehouse-duckdb-iceberg)



## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Conceitos](#conceitos)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Uso](#instalação-e-uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Acessando os Serviços](#acessando-os-serviços)
- [Notebooks Jupyter](#notebooks-jupyter)
- [Exemplos de Uso](#exemplos-de-uso)
- [Comparação com Databricks](#comparação-com-databricks)

## 🎯 Visão Geral

Este projeto implementa um **Lakehouse 100% open source** completo em ambiente local usando:

- **DuckDB**: Engine analítico in-memory otimizado para OLAP
- **Apache Iceberg**: Tabela format para versionamento e time travel
- **MinIO**: Storage S3-compatible para simular cloud storage
- **dbt**: Ferramenta de transformação de dados (ELT)
- **Jupyter Lab**: Ambiente de notebooks integrado para análise e exploração
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

<p align="center">
  <img src="https://raw.githubusercontent.com/aureliowozhiak/modern-lakehouse-duckdb-iceberg/main/docs/lakehouse-diagram.png" alt="Arquitetura do Lakehouse" width="800"/>
</p>

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

#### Implementação no Projeto

Este projeto implementa **Iceberg real** usando:

1. **Tabela DuckDB** (`vendas_iceberg`): Tabela persistente no DuckDB para uso imediato
2. **Tabela Iceberg Real** (`s3://lakehouse/iceberg/vendas_real/`): Estrutura Iceberg completa com:
   - Metadados versionados (`metadata/*.metadata.json`)
   - Arquivos de dados Parquet (`data/*.parquet`)
   - Snapshots para time travel
   - Estrutura de diretórios compatível com Iceberg

**Script disponível:**
- `create_real_iceberg_table.py`: Cria tabela Iceberg REAL com metadados completos

📖 **Para mais detalhes técnicos sobre a implementação do Iceberg, consulte:** [`scripts/ICEBERG_IMPLEMENTATION.md`](scripts/ICEBERG_IMPLEMENTATION.md)

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
docker compose up
```

**⚠️ Importante**: Execute sem `-d` na primeira vez para ver os logs em tempo real e garantir que tudo está funcionando.

Este comando irá automaticamente:
- ✅ Baixar as imagens necessárias
- ✅ Criar os containers
- ✅ Configurar volumes persistentes
- ✅ Subir MinIO (S3-compatible storage)
- ✅ Subir DuckDB (banco de dados analítico)
- ✅ Subir dbt (ferramenta de transformação)
- ✅ Subir Jupyter Lab (ambiente de notebooks) - http://localhost:8888
- ✅ **Executar automaticamente todos os scripts Python:**
  - Criar bucket no MinIO
  - Gerar 5.000 registros de vendas fake
  - Criar tabela Iceberg `vendas_iceberg`
  - Inserir dados na tabela
  - Executar queries de exemplo
- ✅ **Executar automaticamente transformações dbt:**
  - Modelos staging (limpeza de dados)
  - Modelos marts (modelos analíticos)
  - Testes de qualidade de dados

### 3. Processo Automático de Inicialização

O sistema executa automaticamente na seguinte ordem:

#### Etapa 1: MinIO (Storage)
- MinIO sobe e fica disponível nas portas 9000 (API) e 9001 (Console)
- Healthcheck garante que está pronto antes de continuar

#### Etapa 2: DuckDB (Banco de Dados)
- Container DuckDB sobe e fica aguardando conexões
- Volume compartilhado `/app/lakehouse` é criado para persistir dados

#### Etapa 3: Inicialização (init-service)
O serviço `init` executa automaticamente os seguintes scripts Python:

1. **`generate_fake_data.py`**
   - Gera 5.000 registros de vendas simulados
   - Salva em formato Parquet em `/app/data/vendas_raw.parquet`
   - Dados incluem: produtos, clientes, transações, descontos, etc.

2. **`create_real_iceberg_table.py`**
   - Cria tabela **Iceberg REAL** com metadados completos
   - Gera estrutura Iceberg no MinIO (`s3://lakehouse/iceberg/vendas_real/`)
   - Cria tabela DuckDB `vendas_iceberg` para compatibilidade
   - Insere dados e cria snapshots iniciais

3. **`example_queries.py`**
   - Executa 8 queries analíticas de exemplo:
     - Receita por categoria
     - Tendência de vendas mensal
     - Top clientes
     - Análise por canal
     - Time travel (demonstração)
     - Schema evolution (demonstração)
     - Performance de produtos
     - Análise regional

#### Etapa 4: Transformações dbt (dbt-run-service)
Após a inicialização estar completa, o serviço `dbt-run` executa automaticamente:

1. **`dbt run`**
   - Executa todos os modelos dbt na ordem de dependência:
     - **Staging**: `stg_vendas` (limpeza e padronização)
     - **Marts**: 
       - `fct_vendas` (fato de vendas)
       - `dim_produtos` (dimensão de produtos)
       - `dim_clientes` (dimensão de clientes)
       - `mart_vendas_mensal` (agregação mensal)

2. **`dbt test`**
   - Executa testes de qualidade de dados:
     - Verifica unicidade de chaves
     - Verifica valores não nulos
     - Valida integridade referencial

### 4. Verificar Status

```bash
# Ver logs de todos os serviços
docker compose logs -f

# Ver logs de um serviço específico
docker compose logs -f init        # Inicialização
docker compose logs -f dbt-run     # Transformações dbt

# Verificar status dos containers
docker compose ps
```

### 5. Tempo Estimado

- **MinIO e DuckDB**: ~10-20 segundos
- **Inicialização (scripts Python)**: ~1-2 minutos
- **Transformações dbt**: ~30 segundos
- **Total**: ~2-3 minutos

### 6. Verificar Sucesso

Após a inicialização, você deve ver mensagens como:

```
✓ INICIALIZAÇÃO CONCLUÍDA COM SUCESSO!
✓ dbt executado com sucesso!
```

Se tudo funcionou corretamente, você pode:
- Acessar MinIO Console: http://localhost:9001
- Acessar Jupyter Lab: http://localhost:8888
- Executar queries adicionais no DuckDB
- Explorar os modelos dbt criados
- Abrir notebooks para análise interativa

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
│   ├── generate_fake_data.py        # Gera dados fake
│   ├── create_real_iceberg_table.py # Cria tabela Iceberg REAL
│   ├── example_queries.py           # Queries de exemplo
│   └── init_lakehouse.py            # Script de inicialização
├── notebooks/                  # Notebooks Jupyter
│   ├── test_duckdb_connection.ipynb  # Notebook de teste
│   └── README.md              # Documentação dos notebooks
├── data/                       # Dados gerados (volumes)
├── docker-compose.yml          # Orquestração dos serviços
└── README.md                   # Este arquivo
```

## ⚙️ Funcionalidades

### ✅ Funcionalidades Implementadas e Automatizadas

1. **Criação Automática de Bucket**
   - Bucket `lakehouse` criado automaticamente no MinIO durante inicialização
   - Configuração S3-compatible pronta para uso

2. **Geração Automática de Dados Fake**
   - 5.000 registros de vendas simulados gerados automaticamente
   - Dados realistas com produtos, clientes, descontos, canais de venda, etc
   - Período: 2023-2024 com distribuição realista

3. **Criação Automática de Tabela Iceberg**
   - Tabela `vendas_iceberg` criada automaticamente no DuckDB
   - Dados inseridos automaticamente do arquivo Parquet gerado
   - Banco de dados persistente em volume compartilhado

4. **Execução Automática de Queries Analíticas**
   - 8 queries de exemplo executadas automaticamente durante inicialização:
     - Receita por categoria
     - Tendência de vendas mensal
     - Top clientes
     - Análise por canal
     - Time travel (demonstração)
     - Schema evolution (demonstração)
     - Performance de produtos
     - Análise regional

5. **Transformações dbt Automáticas**
   - Modelos staging (limpeza) executados automaticamente
   - Modelos marts (análise) executados automaticamente
   - Dimensões e fatos criados automaticamente
   - Testes de qualidade executados automaticamente

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

## 📓 Notebooks Jupyter

O projeto inclui um ambiente **Jupyter Lab** totalmente integrado com o ecossistema do Lakehouse, permitindo análise interativa e exploração de dados.

### Acessar Jupyter Lab

**URL**: http://localhost:8888

O Jupyter Lab inicia automaticamente quando você executa `docker compose up`. Não requer autenticação (apenas para desenvolvimento local).

### Funcionalidades

- ✅ **Conexão direta ao DuckDB**: Acesse o banco de dados compartilhado
- ✅ **Integração com MinIO**: Configure e acesse dados no MinIO via S3
- ✅ **Acesso às tabelas do dbt**: Consulte modelos transformados (dim_*, fct_*, mart_*)
- ✅ **Visualizações**: Bibliotecas matplotlib, seaborn e plotly incluídas
- ✅ **Scripts disponíveis**: Acesso aos scripts Python do projeto

### Notebooks Disponíveis

- **`test_duckdb_connection.ipynb`**: Notebook de teste que demonstra:
  - Conexão com DuckDB e MinIO
  - Execução de queries baseadas em `scripts/example_queries.py`
  - Visualizações de dados
  - Verificação de tabelas do dbt

### Iniciar o Serviço

```bash
# Iniciar apenas o Jupyter (e dependências)
docker compose up -d jupyter

# Ou iniciar tudo
docker compose up -d
```

### Estrutura de Volumes

Os notebooks têm acesso a:
- `./notebooks` → `/app/notebooks` - Seus notebooks
- `./scripts` → `/app/scripts` - Scripts Python do projeto
- `./data` → `/app/data` - Dados brutos
- `./dbt` → `/app/dbt` - Projeto dbt
- `lakehouse_data` → `/app/lakehouse` - Banco DuckDB compartilhado

### Exemplo Rápido

```python
import duckdb
import os

# Conectar ao DuckDB compartilhado
con = duckdb.connect("/app/lakehouse/lakehouse.duckdb")

# Executar query
df = con.execute("SELECT * FROM vendas_iceberg LIMIT 10").fetchdf()
print(df)
```

📖 **Para mais detalhes, consulte o [README dos notebooks](notebooks/README.md)**

## 💡 Exemplos de Uso

### ⚡ Tudo é Automático!

**Importante**: Todos os scripts Python e transformações dbt são executados automaticamente quando você roda `docker compose up`. Você não precisa executar nada manualmente!

### 1. Re-executar Queries de Exemplo (Opcional)

Se quiser executar as queries novamente:

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

### 2. Re-executar Transformações dbt (Opcional)

Se quiser executar as transformações dbt novamente:

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

### 4. Adicionar Mais Dados (Opcional)

Se quiser gerar mais dados além dos 5.000 iniciais:

```bash
# Gerar mais dados (edite o script para alterar quantidade)
docker compose exec duckdb python /app/scripts/generate_fake_data.py

# Inserir na tabela Iceberg
docker compose exec duckdb python -c "
import duckdb
con = duckdb.connect('/app/lakehouse/lakehouse.duckdb')
con.execute('INSTALL httpfs; LOAD httpfs;')
con.execute('INSTALL iceberg; LOAD iceberg;')
con.execute(\"SET s3_endpoint='minio:9000';\")
con.execute(\"SET s3_access_key_id='admin';\")
con.execute(\"SET s3_secret_access_key='minioadmin123';\")
con.execute(\"SET s3_use_ssl=false;\")
con.execute(\"SET s3_url_style='path';\")
con.execute(\"INSERT INTO vendas_iceberg SELECT * FROM read_parquet('/app/data/vendas_raw.parquet');\")
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
| **UI** | Databricks Notebooks | Jupyter Lab / Docker CLI / MinIO Console |

### Vantagens deste Projeto (100% Open Source)

- ✅ **100% Local**: Roda completamente offline
- ✅ **Zero Custo**: Sem necessidade de cloud ou licenças
- ✅ **100% Open Source**: Todas as tecnologias são open source (DuckDB, Iceberg, MinIO, dbt, Jupyter)
- ✅ **Educacional**: Ideal para aprender conceitos de Lakehouse
- ✅ **Rápido Setup**: `docker compose up` e pronto
- ✅ **Alternativa Open Source**: Substitui soluções proprietárias como Databricks

### Limitações vs Databricks

- ⚠️ **Escala**: Limitado a máquina local (vs cluster distribuído)
- ⚠️ **Colaboração**: Notebooks locais (vs notebooks compartilhados na nuvem)
- ⚠️ **ML**: Sem MLflow integrado
- ⚠️ **Governança**: Sem Unity Catalog
- ⚠️ **Performance**: DuckDB é single-node (vs Spark distribuído)

## 🛠️ Troubleshooting

### Problema: MinIO não inicia

**Sintomas**: Container minio para ou não responde

**Solução**:
```bash
# Verificar logs
docker compose logs minio

# Verificar se a porta está em uso
netstat -an | grep 9000

# Reiniciar serviço
docker compose restart minio

# Se persistir, recriar volumes
docker compose down -v
docker compose up
```

### Problema: Tabela Iceberg não encontrada

**Sintomas**: Erro "Table 'vendas_iceberg' not found" ao executar queries

**Solução**:
```bash
# Verificar se a inicialização foi concluída
docker compose logs init

# Re-executar inicialização completa
docker compose down
docker compose up init

# Verificar se o banco foi criado
docker compose exec duckdb ls -lh /app/lakehouse/
```

### Problema: Erro de conexão S3

**Sintomas**: Erro ao conectar ao MinIO (timeout, connection refused)

**Solução**:
```bash
# Verificar se MinIO está rodando
docker compose ps minio

# Verificar healthcheck
docker compose exec minio curl -f http://localhost:9000/minio/health/live

# Verificar variáveis de ambiente
docker compose config | grep MINIO
```

### Problema: dbt não encontra tabela

**Sintomas**: Erro "Table 'vendas_iceberg' does not exist" no dbt

**Solução**:
```bash
# Verificar logs da inicialização
docker compose logs init

# Verificar se o banco existe
docker compose exec dbt-run ls -lh /app/lakehouse/

# Re-executar inicialização e dbt
docker compose up init
docker compose up dbt-run
```

### Problema: Scripts Python falham

**Sintomas**: Erros ao executar scripts de inicialização

**Solução**:
```bash
# Verificar logs detalhados
docker compose logs init

# Executar script manualmente para debug
docker compose exec duckdb python /app/scripts/generate_fake_data.py
docker compose exec duckdb python /app/scripts/create_real_iceberg_table.py

# Verificar dependências
docker compose exec duckdb pip list
```

### Problema: dbt run falha

**Sintomas**: Erro ao executar `dbt run`

**Solução**:
```bash
# Verificar logs
docker compose logs dbt-run

# Executar dbt manualmente para debug
docker compose exec dbt dbt debug
docker compose exec dbt dbt run --select staging
docker compose exec dbt dbt run --select marts

# Verificar se o banco está acessível
docker compose exec dbt python -c "import duckdb; con = duckdb.connect('/app/lakehouse/lakehouse.duckdb'); print(con.execute('SELECT COUNT(*) FROM vendas_iceberg').fetchone())"
```

### Problema: Containers param imediatamente

**Sintomas**: Containers iniciam e param logo em seguida

**Solução**:
```bash
# Verificar logs de todos os serviços
docker compose logs

# Verificar status
docker compose ps -a

# Recriar tudo do zero
docker compose down -v
docker compose build --no-cache
docker compose up
```

### Limpar tudo e começar do zero

Se nada funcionar, limpe tudo e recomece:

```bash
# Parar e remover tudo
docker compose down -v

# Remover imagens (opcional)
docker compose down --rmi all

# Reconstruir e iniciar
docker compose build --no-cache
docker compose up
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

### Documentação Externa

- [Apache Iceberg](https://iceberg.apache.org/)
- [DuckDB](https://duckdb.org/)
- [MinIO](https://min.io/)
- [dbt](https://www.getdbt.com/)
- [Databricks Lakehouse](https://www.databricks.com/product/data-lakehouse)

### Documentação do Projeto

- [Implementação Apache Iceberg](scripts/ICEBERG_IMPLEMENTATION.md) - Detalhes técnicos sobre a implementação do Iceberg neste projeto

---

**Desenvolvido com ❤️ para aprendizado de engenharia de dados modernos**
