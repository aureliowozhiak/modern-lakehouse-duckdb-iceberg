# Implementação Apache Iceberg Real

Este documento explica como o Apache Iceberg está implementado neste projeto.

## Estrutura

O projeto implementa **Iceberg REAL** com metadados completos.

### Tabela Iceberg Real (Metadados Completos)

**Script**: `create_real_iceberg_table.py` ⭐ **SCRIPT PRINCIPAL**

- Cria estrutura Iceberg completa com metadados
- Gera arquivos `metadata.json` com schema, snapshots e versionamento
- Cria tabela DuckDB `vendas_iceberg` para compatibilidade e leitura
- Estrutura de diretórios compatível com Iceberg
- Estrutura: `s3://lakehouse/iceberg/vendas_real/`


- Cria estrutura Iceberg completa com metadados
- Gera arquivos `metadata.json` com schema, snapshots e versionamento
- Estrutura de diretórios compatível com Iceberg
- Estrutura: `s3://lakehouse/iceberg/vendas_real/`

```
s3://lakehouse/iceberg/vendas_real/
├── data/
│   └── data-00000.parquet          # Dados em formato Parquet
└── metadata/
    └── *.metadata.json              # Metadados Iceberg versionados
```

## Características Implementadas

### ✅ Implementado

- **Estrutura de Diretórios**: Compatível com padrão Iceberg
- **Metadados Versionados**: Arquivos `metadata.json` com schema e snapshots
- **Formato Parquet**: Dados armazenados em Parquet
- **Integração S3**: Armazenamento no MinIO (S3-compatible)
- **Compatibilidade DuckDB**: Tabela DuckDB para leitura imediata

### ⚠️ Limitações Atuais

- **Time Travel**: Estrutura criada, mas requer catalog Iceberg completo para uso
- **Schema Evolution**: Metadados suportam, mas requer catalog para alterações
- **ACID Transactions**: Estrutura básica, catalog completo necessário para transações complexas

## Como Usar

### Execução Automática

O script `create_real_iceberg_table.py` é executado automaticamente durante a inicialização:

```bash
docker compose up
```

### Execução Manual

```bash
# Criar tabela Iceberg real
docker compose exec duckdb python /app/scripts/create_real_iceberg_table.py
```

### Verificar Estrutura

1. **MinIO Console**: http://localhost:9001
   - Navegue até `lakehouse/iceberg/vendas_real/`
   - Veja a estrutura de diretórios e metadados

2. **Via DuckDB**:
```python
import duckdb
con = duckdb.connect("/app/lakehouse/lakehouse.duckdb")
# Configurar S3...
# Ler dados da tabela Iceberg
```

## Próximos Passos

Para funcionalidades completas de Iceberg:

1. **Catalog REST Server**: Implementar catalog Iceberg REST para gerenciamento completo
2. **Time Travel**: Usar catalog para acessar snapshots anteriores
3. **Schema Evolution**: Usar catalog para evoluir schema sem quebrar compatibilidade
4. **ACID Completo**: Catalog garante transações ACID completas

## Referências

- [Apache Iceberg Specification](https://iceberg.apache.org/spec/)
- [PyIceberg Documentation](https://py.iceberg.apache.org/)
- [DuckDB Iceberg Extension](https://duckdb.org/docs/extensions/iceberg)

