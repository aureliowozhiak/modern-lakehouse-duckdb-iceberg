{{
    config(
        materialized='table',
        description='Mart de vendas agregado por mês'
    )
}}

-- Mart de vendas mensal: Agregação mensal para dashboards
SELECT
    DATE_TRUNC('month', data_venda) as mes,
    EXTRACT(YEAR FROM data_venda) as ano,
    EXTRACT(MONTH FROM data_venda) as mes_numero,
    
    -- Métricas de vendas
    COUNT(*) as total_vendas,
    COUNT(DISTINCT cliente_id) as clientes_unicos,
    COUNT(DISTINCT produto_id) as produtos_vendidos,
    
    -- Métricas financeiras
    SUM(valor_final) as receita_total,
    AVG(valor_final) as ticket_medio,
    SUM(quantidade) as unidades_vendidas,
    SUM(valor_desconto) as total_descontos,
    AVG(desconto_percentual) as desconto_medio_percentual,
    
    -- Análises por categoria
    SUM(CASE WHEN categoria = 'eletrônicos' THEN valor_final ELSE 0 END) as receita_eletronicos,
    SUM(CASE WHEN categoria = 'periféricos' THEN valor_final ELSE 0 END) as receita_perifericos,
    SUM(CASE WHEN categoria = 'componentes' THEN valor_final ELSE 0 END) as receita_componentes,
    
    -- Análises por canal
    SUM(CASE WHEN canal_venda = 'Online' THEN valor_final ELSE 0 END) as receita_online,
    SUM(CASE WHEN canal_venda = 'Loja Física' THEN valor_final ELSE 0 END) as receita_loja,
    
    -- Crescimento (comparação com mês anterior - será calculado em outra camada)
    NULL as receita_mes_anterior,
    NULL as crescimento_percentual
    
FROM {{ ref('fct_vendas') }}
GROUP BY DATE_TRUNC('month', data_venda), EXTRACT(YEAR FROM data_venda), EXTRACT(MONTH FROM data_venda)
ORDER BY mes

