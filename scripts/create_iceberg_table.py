"""
Script para criar tabela Apache Iceberg no DuckDB usando MinIO como storage.
Demonstra criação de tabela Iceberg com particionamento e configurações otimizadas.
"""

import duckdb
import os
import sys
from datetime import datetime

def setup_s3_connection(con):
    """
    Configura conexão S3 (MinIO) no DuckDB.
    
    Args:
        con: Conexão DuckDB
    """
    minio_endpoint = os.getenv('MINIO_ENDPOINT', 'minio:9000')
    minio_access_key = os.getenv('MINIO_ACCESS_KEY', 'admin')
    minio_secret_key = os.getenv('MINIO_SECRET_KEY', 'minioadmin123')
    minio_bucket = os.getenv('MINIO_BUCKET', 'lakehouse')
    
    print("Configurando conexão S3 (MinIO)...")
    
    # Configurar S3 no DuckDB
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
    
    print(f"✓ Conexão S3 configurada: s3://{minio_bucket}/")
    return f"s3://{minio_bucket}"

def create_bucket_if_not_exists(con, bucket_name):
    """
    Cria bucket no MinIO se não existir.
    Nota: DuckDB não tem comando direto para criar bucket,
    então assumimos que o bucket será criado pelo MinIO ou já existe.
    """
    print(f"Verificando bucket '{bucket_name}'...")
    # O bucket será criado automaticamente quando escrevermos dados
    print(f"✓ Bucket '{bucket_name}' será usado")

def create_iceberg_table(con, s3_path):
    """
    Cria tabela Iceberg no DuckDB.
    
    Args:
        con: Conexão DuckDB
        s3_path: Caminho S3 base (s3://bucket)
    """
    table_path = f"{s3_path}/iceberg/vendas"
    
    print("\n" + "="*80)
    print("Criando tabela Iceberg: vendas")
    print("="*80)
    
    # Criar tabela Iceberg
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS vendas_iceberg (
        venda_id VARCHAR,
        data_venda DATE,
        timestamp_venda TIMESTAMP,
        produto_id INTEGER,
        produto_nome VARCHAR,
        categoria VARCHAR,
        preco_unitario DECIMAL(10,2),
        quantidade INTEGER,
        valor_total DECIMAL(10,2),
        desconto_percentual DECIMAL(5,2),
        valor_desconto DECIMAL(10,2),
        valor_final DECIMAL(10,2),
        cliente_id INTEGER,
        cliente_nome VARCHAR,
        cliente_email VARCHAR,
        cliente_cidade VARCHAR,
        cliente_estado VARCHAR,
        canal_venda VARCHAR,
        status VARCHAR
    ) USING ICEBERG (
        LOCATION '{table_path}',
        PARTITION_BY (YEAR(data_venda), MONTH(data_venda))
    );
    """
    
    try:
        con.execute(create_table_sql)
        print("✓ Tabela Iceberg criada com sucesso!")
        print(f"  Localização: {table_path}")
        print(f"  Particionamento: YEAR(data_venda), MONTH(data_venda)")
    except Exception as e:
        print(f"⚠ Erro ao criar tabela: {e}")
        print("Tentando criar sem particionamento...")
        
        # Fallback: criar sem particionamento
        create_table_sql_fallback = f"""
        CREATE TABLE IF NOT EXISTS vendas_iceberg (
            venda_id VARCHAR,
            data_venda DATE,
            timestamp_venda TIMESTAMP,
            produto_id INTEGER,
            produto_nome VARCHAR,
            categoria VARCHAR,
            preco_unitario DECIMAL(10,2),
            quantidade INTEGER,
            valor_total DECIMAL(10,2),
            desconto_percentual DECIMAL(5,2),
            valor_desconto DECIMAL(10,2),
            valor_final DECIMAL(10,2),
            cliente_id INTEGER,
            cliente_nome VARCHAR,
            cliente_email VARCHAR,
            cliente_cidade VARCHAR,
            cliente_estado VARCHAR,
            canal_venda VARCHAR,
            status VARCHAR
        ) USING ICEBERG (
            LOCATION '{table_path}'
        );
        """
        con.execute(create_table_sql_fallback)
        print("✓ Tabela Iceberg criada (sem particionamento)!")

def insert_data_from_parquet(con, parquet_path):
    """
    Insere dados do arquivo Parquet na tabela Iceberg.
    
    Args:
        con: Conexão DuckDB
        parquet_path: Caminho do arquivo Parquet
    """
    print("\n" + "="*80)
    print("Inserindo dados na tabela Iceberg...")
    print("="*80)
    
    if not os.path.exists(parquet_path):
        print(f"⚠ Arquivo não encontrado: {parquet_path}")
        return
    
    # Inserir dados
    insert_sql = f"""
    INSERT INTO vendas_iceberg
    SELECT 
        venda_id,
        CAST(data_venda AS DATE) as data_venda,
        CAST(timestamp_venda AS TIMESTAMP) as timestamp_venda,
        produto_id,
        produto_nome,
        categoria,
        preco_unitario,
        quantidade,
        valor_total,
        desconto_percentual,
        valor_desconto,
        valor_final,
        cliente_id,
        cliente_nome,
        cliente_email,
        cliente_cidade,
        cliente_estado,
        canal_venda,
        status
    FROM read_parquet('{parquet_path}');
    """
    
    try:
        con.execute(insert_sql)
        # Contar registros inseridos
        count = con.execute("SELECT COUNT(*) FROM vendas_iceberg").fetchone()[0]
        print(f"✓ Dados inseridos com sucesso!")
        print(f"  Total de registros na tabela: {count:,}")
    except Exception as e:
        print(f"⚠ Erro ao inserir dados: {e}")
        raise

def verify_table(con):
    """
    Verifica a tabela criada e mostra estatísticas.
    
    Args:
        con: Conexão DuckDB
    """
    print("\n" + "="*80)
    print("Verificando tabela Iceberg...")
    print("="*80)
    
    # Contar registros
    count_result = con.execute("SELECT COUNT(*) FROM vendas_iceberg").fetchone()
    print(f"✓ Total de registros: {count_result[0]:,}")
    
    # Estatísticas básicas
    stats_sql = """
    SELECT 
        COUNT(*) as total_vendas,
        SUM(valor_final) as receita_total,
        AVG(valor_final) as ticket_medio,
        MIN(data_venda) as primeira_venda,
        MAX(data_venda) as ultima_venda,
        COUNT(DISTINCT cliente_id) as clientes_unicos,
        COUNT(DISTINCT categoria) as categorias
    FROM vendas_iceberg;
    """
    
    stats = con.execute(stats_sql).fetchone()
    print(f"\nEstatísticas:")
    print(f"  - Receita Total: R$ {stats[1]:,.2f}")
    print(f"  - Ticket Médio: R$ {stats[2]:,.2f}")
    print(f"  - Período: {stats[3]} até {stats[4]}")
    print(f"  - Clientes Únicos: {stats[5]:,}")
    print(f"  - Categorias: {stats[6]}")

def main():
    """Função principal."""
    print("="*80)
    print("CRIAÇÃO DE TABELA ICEBERG NO DUCKDB")
    print("="*80)
    
    # Conectar ao DuckDB
    con = duckdb.connect()
    
    try:
        # Configurar S3
        s3_path = setup_s3_connection(con)
        bucket_name = os.getenv('MINIO_BUCKET', 'lakehouse')
        create_bucket_if_not_exists(con, bucket_name)
        
        # Criar tabela Iceberg
        create_iceberg_table(con, s3_path)
        
        # Inserir dados
        parquet_path = "/app/data/vendas_raw.parquet"
        if os.path.exists(parquet_path):
            insert_data_from_parquet(con, parquet_path)
        else:
            print(f"⚠ Arquivo Parquet não encontrado: {parquet_path}")
            print("Execute primeiro o script generate_fake_data.py")
        
        # Verificar tabela
        verify_table(con)
        
        print("\n" + "="*80)
        print("✓ Processo concluído com sucesso!")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        con.close()

if __name__ == "__main__":
    main()

