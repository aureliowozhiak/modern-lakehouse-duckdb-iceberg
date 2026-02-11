"""
Script com exemplos de queries analíticas usando DuckDB e Apache Iceberg.
Demonstra time travel, schema evolution e análises de negócio.
"""

import duckdb
import os
from datetime import datetime, timedelta

def setup_connection():
    """
    Configura conexão DuckDB com S3 (MinIO).
    
    Returns:
        Conexão DuckDB configurada
    """
    con = duckdb.connect()
    
    minio_endpoint = os.getenv('MINIO_ENDPOINT', 'minio:9000')
    minio_access_key = os.getenv('MINIO_ACCESS_KEY', 'admin')
    minio_secret_key = os.getenv('MINIO_SECRET_KEY', 'minioadmin123')
    
    con.execute(f"""
        INSTALL httpfs;
        LOAD httpfs;
        INSTALL iceberg;
        LOAD iceberg;
        SET s3_endpoint='{minio_endpoint}';
        SET s3_access_key_id='{minio_access_key}';
        SET s3_secret_access_key='{minio_secret_key}';
        SET s3_use_ssl=false;
        SET s3_url_style='path';
    """)
    
    return con

def query_1_revenue_by_category(con):
    """
    Query 1: Receita por categoria de produto.
    """
    print("\n" + "="*80)
    print("QUERY 1: Receita por Categoria")
    print("="*80)
    
    sql = """
    SELECT 
        categoria,
        COUNT(*) as total_vendas,
        SUM(valor_final) as receita_total,
        AVG(valor_final) as ticket_medio,
        SUM(quantidade) as unidades_vendidas
    FROM vendas_iceberg
    WHERE status = 'Concluída'
    GROUP BY categoria
    ORDER BY receita_total DESC;
    """
    
    result = con.execute(sql).fetchdf()
    print(result.to_string(index=False))
    return result

def query_2_sales_trend(con):
    """
    Query 2: Tendência de vendas ao longo do tempo (mensal).
    """
    print("\n" + "="*80)
    print("QUERY 2: Tendência de Vendas Mensal")
    print("="*80)
    
    sql = """
    SELECT 
        DATE_TRUNC('month', data_venda) as mes,
        COUNT(*) as total_vendas,
        SUM(valor_final) as receita_mensal,
        AVG(valor_final) as ticket_medio,
        COUNT(DISTINCT cliente_id) as clientes_unicos
    FROM vendas_iceberg
    WHERE status = 'Concluída'
    GROUP BY DATE_TRUNC('month', data_venda)
    ORDER BY mes;
    """
    
    result = con.execute(sql).fetchdf()
    print(result.to_string(index=False))
    return result

def query_3_top_customers(con, limit=10):
    """
    Query 3: Top clientes por valor de compra.
    """
    print("\n" + "="*80)
    print(f"QUERY 3: Top {limit} Clientes")
    print("="*80)
    
    sql = f"""
    SELECT 
        cliente_id,
        cliente_nome,
        cliente_cidade,
        cliente_estado,
        COUNT(*) as total_compras,
        SUM(valor_final) as valor_total_gasto,
        AVG(valor_final) as ticket_medio
    FROM vendas_iceberg
    WHERE status = 'Concluída'
    GROUP BY cliente_id, cliente_nome, cliente_cidade, cliente_estado
    ORDER BY valor_total_gasto DESC
    LIMIT {limit};
    """
    
    result = con.execute(sql).fetchdf()
    print(result.to_string(index=False))
    return result

def query_4_channel_analysis(con):
    """
    Query 4: Análise por canal de venda.
    """
    print("\n" + "="*80)
    print("QUERY 4: Análise por Canal de Venda")
    print("="*80)
    
    sql = """
    SELECT 
        canal_venda,
        COUNT(*) as total_vendas,
        SUM(valor_final) as receita_total,
        AVG(valor_final) as ticket_medio,
        SUM(valor_desconto) as total_descontos,
        AVG(desconto_percentual) as desconto_medio_percentual
    FROM vendas_iceberg
    WHERE status = 'Concluída'
    GROUP BY canal_venda
    ORDER BY receita_total DESC;
    """
    
    result = con.execute(sql).fetchdf()
    print(result.to_string(index=False))
    return result

def query_5_time_travel_example(con):
    """
    Query 5: Demonstração de Time Travel (se suportado).
    Nota: Time travel requer snapshots do Iceberg.
    """
    print("\n" + "="*80)
    print("QUERY 5: Time Travel - Estado da Tabela em Diferentes Momentos")
    print("="*80)
    
    # Primeiro, vamos contar registros atuais
    current_count = con.execute("SELECT COUNT(*) FROM vendas_iceberg").fetchone()[0]
    print(f"Registros atuais: {current_count:,}")
    
    # Tentar acessar histórico (se disponível)
    try:
        # Nota: A sintaxe de time travel pode variar
        # Esta é uma demonstração conceitual
        print("\nTime Travel permite acessar versões anteriores da tabela.")
        print("No Iceberg, cada operação cria um snapshot que pode ser consultado.")
        print("\nExemplo conceitual:")
        print("  SELECT * FROM vendas_iceberg FOR TIMESTAMP AS OF '2024-01-01'")
        print("  SELECT * FROM vendas_iceberg FOR VERSION AS OF 1")
    except Exception as e:
        print(f"Time travel não disponível ou requer configuração adicional: {e}")

def query_6_schema_evolution_demo(con):
    """
    Query 6: Demonstração de Schema Evolution.
    Adiciona uma nova coluna calculada.
    """
    print("\n" + "="*80)
    print("QUERY 6: Schema Evolution - Adicionando Coluna Calculada")
    print("="*80)
    
    # Iceberg suporta schema evolution - podemos adicionar colunas sem recriar a tabela
    # Por enquanto, vamos criar uma view com a nova coluna
    sql = """
    CREATE OR REPLACE VIEW vendas_enriquecidas AS
    SELECT 
        *,
        CASE 
            WHEN valor_final >= 1000 THEN 'Alto Valor'
            WHEN valor_final >= 500 THEN 'Médio Valor'
            ELSE 'Baixo Valor'
        END as segmento_valor,
        CASE 
            WHEN desconto_percentual > 10 THEN 'Com Desconto Significativo'
            WHEN desconto_percentual > 0 THEN 'Com Desconto Pequeno'
            ELSE 'Sem Desconto'
        END as tipo_desconto
    FROM vendas_iceberg;
    """
    
    try:
        con.execute(sql)
        print("✓ View criada com colunas calculadas (simulando schema evolution)")
        
        # Query usando a view
        result = con.execute("""
            SELECT 
                segmento_valor,
                tipo_desconto,
                COUNT(*) as total,
                AVG(valor_final) as ticket_medio
            FROM vendas_enriquecidas
            GROUP BY segmento_valor, tipo_desconto
            ORDER BY segmento_valor, tipo_desconto;
        """).fetchdf()
        
        print("\nResultado:")
        print(result.to_string(index=False))
    except Exception as e:
        print(f"⚠ Erro: {e}")

def query_7_product_performance(con):
    """
    Query 7: Performance de produtos.
    """
    print("\n" + "="*80)
    print("QUERY 7: Performance de Produtos")
    print("="*80)
    
    sql = """
    SELECT 
        produto_id,
        produto_nome,
        categoria,
        COUNT(*) as vezes_vendido,
        SUM(quantidade) as unidades_vendidas,
        SUM(valor_final) as receita_total,
        AVG(preco_unitario) as preco_medio,
        MIN(data_venda) as primeira_venda,
        MAX(data_venda) as ultima_venda
    FROM vendas_iceberg
    WHERE status = 'Concluída'
    GROUP BY produto_id, produto_nome, categoria
    ORDER BY receita_total DESC
    LIMIT 10;
    """
    
    result = con.execute(sql).fetchdf()
    print(result.to_string(index=False))
    return result

def query_8_regional_analysis(con):
    """
    Query 8: Análise regional.
    """
    print("\n" + "="*80)
    print("QUERY 8: Análise Regional")
    print("="*80)
    
    sql = """
    SELECT 
        cliente_estado,
        COUNT(DISTINCT cliente_id) as clientes_unicos,
        COUNT(*) as total_vendas,
        SUM(valor_final) as receita_total,
        AVG(valor_final) as ticket_medio
    FROM vendas_iceberg
    WHERE status = 'Concluída'
    GROUP BY cliente_estado
    ORDER BY receita_total DESC;
    """
    
    result = con.execute(sql).fetchdf()
    print(result.to_string(index=False))
    return result

def main():
    """Executa todas as queries de exemplo."""
    print("="*80)
    print("EXEMPLOS DE QUERIES ANALÍTICAS - DUCKDB + ICEBERG")
    print("="*80)
    
    con = setup_connection()
    
    try:
        # Verificar se a tabela existe
        try:
            count = con.execute("SELECT COUNT(*) FROM vendas_iceberg").fetchone()[0]
            print(f"\n✓ Tabela encontrada com {count:,} registros\n")
        except Exception as e:
            print(f"\n❌ Tabela 'vendas_iceberg' não encontrada!")
            print("Execute primeiro o script create_iceberg_table.py")
            return
        
        # Executar queries
        query_1_revenue_by_category(con)
        query_2_sales_trend(con)
        query_3_top_customers(con)
        query_4_channel_analysis(con)
        query_5_time_travel_example(con)
        query_6_schema_evolution_demo(con)
        query_7_product_performance(con)
        query_8_regional_analysis(con)
        
        print("\n" + "="*80)
        print("✓ Todas as queries executadas com sucesso!")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        con.close()

if __name__ == "__main__":
    main()

