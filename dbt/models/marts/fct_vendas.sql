{{
    config(
        materialized='table',
        description='Fato de vendas com métricas de negócio'
    )
}}

-- Fato de vendas: Tabela principal para análises
SELECT
    venda_id,
    data_venda,
    timestamp_venda,
    
    -- Dimensões de produto
    produto_id,
    produto_nome,
    categoria,
    
    -- Dimensões de cliente
    cliente_id,
    cliente_nome,
    cliente_email,
    cliente_cidade,
    cliente_estado,
    
    -- Dimensões de venda
    canal_venda,
    
    -- Métricas
    preco_unitario,
    quantidade,
    valor_total,
    desconto_percentual,
    valor_desconto,
    valor_final,
    
    -- Métricas calculadas
    valor_final / NULLIF(quantidade, 0) as ticket_medio_item,
    CASE 
        WHEN valor_final >= 1000 THEN 'Alto Valor'
        WHEN valor_final >= 500 THEN 'Médio Valor'
        ELSE 'Baixo Valor'
    END as segmento_valor,
    
    -- Dimensões temporais
    EXTRACT(YEAR FROM data_venda) as ano,
    EXTRACT(QUARTER FROM data_venda) as trimestre,
    EXTRACT(MONTH FROM data_venda) as mes,
    EXTRACT(DAYOFWEEK FROM data_venda) as dia_semana
    
FROM {{ ref('stg_vendas') }}

