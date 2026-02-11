{{
    config(
        materialized='table',
        description='Dimensão de clientes'
    )
}}

-- Dimensão de clientes: Agregação de informações por cliente
SELECT
    cliente_id,
    cliente_nome,
    cliente_email,
    cliente_cidade,
    cliente_estado,
    
    -- Métricas agregadas
    COUNT(*) as total_compras,
    SUM(valor_final) as valor_total_gasto,
    AVG(valor_final) as ticket_medio,
    MIN(data_venda) as primeira_compra,
    MAX(data_venda) as ultima_compra,
    
    -- Análises
    COUNT(DISTINCT categoria) as categorias_compradas,
    COUNT(DISTINCT canal_venda) as canais_utilizados,
    SUM(quantidade) as total_itens_comprados,
    
    -- Segmentação
    CASE 
        WHEN SUM(valor_final) >= 5000 THEN 'VIP'
        WHEN SUM(valor_final) >= 2000 THEN 'Premium'
        WHEN SUM(valor_final) >= 1000 THEN 'Regular'
        ELSE 'Ocasional'
    END as segmento_cliente,
    
    -- Ranking
    ROW_NUMBER() OVER (ORDER BY SUM(valor_final) DESC) as ranking_cliente
    
FROM {{ ref('stg_vendas') }}
GROUP BY cliente_id, cliente_nome, cliente_email, cliente_cidade, cliente_estado

