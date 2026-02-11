# dbt Project - Lakehouse

Este projeto dbt transforma os dados brutos do Iceberg em modelos analíticos estruturados.

## Estrutura

```
models/
  staging/          # Limpeza e padronização
    stg_vendas.sql
  marts/            # Modelos analíticos
    fct_vendas.sql
    dim_produtos.sql
    dim_clientes.sql
    mart_vendas_mensal.sql
```

## Executar

```bash
# Executar todos os modelos
docker compose exec dbt dbt run

# Executar apenas staging
docker compose exec dbt dbt run --select staging

# Executar apenas marts
docker compose exec dbt dbt run --select marts

# Executar testes
docker compose exec dbt dbt test

# Gerar documentação
docker compose exec dbt dbt docs generate
docker compose exec dbt dbt docs serve
```

## Modelos

### Staging
- `stg_vendas`: Dados de vendas limpos e padronizados

### Marts
- `fct_vendas`: Fato de vendas com todas as métricas
- `dim_produtos`: Dimensão de produtos
- `dim_clientes`: Dimensão de clientes
- `mart_vendas_mensal`: Agregação mensal para dashboards

