{{
    config(
        materialized='view'
    )
}}

-- Staging model: Limpeza e padronização dos dados de vendas
SELECT
    venda_id,
    CAST(data_venda AS DATE) as data_venda,
    CAST(timestamp_venda AS TIMESTAMP) as timestamp_venda,
    produto_id,
    LOWER(TRIM(produto_nome)) as produto_nome,
    LOWER(TRIM(categoria)) as categoria,
    CAST(preco_unitario AS DECIMAL(10,2)) as preco_unitario,
    CAST(quantidade AS INTEGER) as quantidade,
    CAST(valor_total AS DECIMAL(10,2)) as valor_total,
    CAST(desconto_percentual AS DECIMAL(5,2)) as desconto_percentual,
    CAST(valor_desconto AS DECIMAL(10,2)) as valor_desconto,
    CAST(valor_final AS DECIMAL(10,2)) as valor_final,
    cliente_id,
    TRIM(cliente_nome) as cliente_nome,
    LOWER(TRIM(cliente_email)) as cliente_email,
    TRIM(cliente_cidade) as cliente_cidade,
    UPPER(TRIM(cliente_estado)) as cliente_estado,
    TRIM(canal_venda) as canal_venda,
    TRIM(status) as status
FROM vendas_iceberg
WHERE status = 'Concluída'  -- Apenas vendas concluídas

