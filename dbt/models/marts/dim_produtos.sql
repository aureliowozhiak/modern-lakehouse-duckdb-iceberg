{{
    config(
        materialized='table',
        description='Dimensão de produtos'
    )
}}

-- Dimensão de produtos: Agregação de informações por produto
SELECT
    produto_id,
    produto_nome,
    categoria,
    
    -- Métricas agregadas
    COUNT(*) as total_vendas,
    SUM(quantidade) as total_unidades_vendidas,
    SUM(valor_final) as receita_total,
    AVG(preco_unitario) as preco_medio,
    AVG(valor_final) as ticket_medio,
    MIN(data_venda) as primeira_venda,
    MAX(data_venda) as ultima_venda,
    
    -- Análises
    AVG(desconto_percentual) as desconto_medio_percentual,
    SUM(CASE WHEN desconto_percentual > 0 THEN 1 ELSE 0 END) as vendas_com_desconto,
    
    -- Ranking
    ROW_NUMBER() OVER (ORDER BY SUM(valor_final) DESC) as ranking_receita
    
FROM {{ ref('stg_vendas') }}
GROUP BY produto_id, produto_nome, categoria

