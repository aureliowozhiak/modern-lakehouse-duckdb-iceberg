"""
Script de inicialização do Lakehouse.
Cria bucket, gera dados, cria tabela Iceberg e insere dados.
"""

import time
import subprocess
import sys
import os

def wait_for_minio(max_retries=30, delay=2):
    """
    Aguarda MinIO estar disponível.
    
    Args:
        max_retries: Número máximo de tentativas
        delay: Delay entre tentativas (segundos)
    """
    try:
        import requests
    except ImportError:
        print("⚠ requests não disponível, pulando verificação do MinIO")
        return False
    
    minio_endpoint = os.getenv('MINIO_ENDPOINT', 'minio:9000')
    url = f"http://{minio_endpoint}/minio/health/live"
    
    print("Aguardando MinIO estar disponível...")
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print("✓ MinIO está disponível!")
                return True
        except:
            pass
        
        if i < max_retries - 1:
            print(f"  Tentativa {i+1}/{max_retries}...")
            time.sleep(delay)
    
    print("⚠ MinIO não está disponível, mas continuando...")
    return False

def create_bucket():
    """
    Cria bucket no MinIO usando boto3.
    """
    import boto3
    from botocore.config import Config
    
    minio_endpoint = os.getenv('MINIO_ENDPOINT', 'minio:9000')
    minio_access_key = os.getenv('MINIO_ACCESS_KEY', 'admin')
    minio_secret_key = os.getenv('MINIO_SECRET_KEY', 'minioadmin123')
    minio_bucket = os.getenv('MINIO_BUCKET', 'lakehouse')
    
    print(f"\nCriando bucket '{minio_bucket}' no MinIO...")
    
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=f'http://{minio_endpoint}',
            aws_access_key_id=minio_access_key,
            aws_secret_access_key=minio_secret_key,
            config=Config(signature_version='s3v4'),
            region_name='us-east-1'
        )
        
        # Criar bucket se não existir
        try:
            s3_client.head_bucket(Bucket=minio_bucket)
            print(f"✓ Bucket '{minio_bucket}' já existe")
        except:
            s3_client.create_bucket(Bucket=minio_bucket)
            print(f"✓ Bucket '{minio_bucket}' criado com sucesso!")
            
    except Exception as e:
        print(f"⚠ Erro ao criar bucket: {e}")
        print("Continuando... (o bucket pode ser criado automaticamente)")

def run_script(script_path, description):
    """
    Executa um script Python.
    
    Args:
        script_path: Caminho do script
        description: Descrição do que o script faz
    """
    print("\n" + "="*80)
    print(f"{description}")
    print("="*80)
    
    if not os.path.exists(script_path):
        print(f"⚠ Script não encontrado: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd="/app"
        )
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"✓ {description} - Concluído!")
            return True
        else:
            print(f"❌ Erro ao executar {script_path}:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Função principal de inicialização."""
    print("="*80)
    print("INICIALIZAÇÃO DO LAKEHOUSE")
    print("="*80)
    print("\nEste script irá:")
    print("  1. Aguardar MinIO estar disponível")
    print("  2. Criar bucket no MinIO")
    print("  3. Gerar dados fake")
    print("  4. Criar tabela Iceberg")
    print("  5. Inserir dados na tabela")
    print("\nAguarde...\n")
    
    # Aguardar MinIO
    try:
        wait_for_minio()
    except ImportError:
        print("⚠ requests não disponível, pulando verificação do MinIO")
    
    # Criar bucket
    try:
        create_bucket()
    except ImportError:
        print("⚠ boto3 não disponível, pulando criação de bucket")
    
    # Aguardar um pouco para garantir que tudo está pronto
    time.sleep(3)
    
    # Executar scripts na ordem
    scripts = [
        ("/app/scripts/generate_fake_data.py", "Gerando dados fake"),
        ("/app/scripts/create_iceberg_table.py", "Criando tabela Iceberg"),
    ]
    
    success = True
    for script_path, description in scripts:
        if not run_script(script_path, description):
            success = False
            print(f"⚠ Falha em: {description}")
            # Continuar mesmo com erros parciais
    
    print("\n" + "="*80)
    if success:
        print("✓ INICIALIZAÇÃO CONCLUÍDA COM SUCESSO!")
        print("\nPróximos passos:")
        print("  1. Acesse MinIO Console: http://localhost:9001")
        print("  2. Execute queries: docker compose exec duckdb python /app/scripts/example_queries.py")
        print("  3. Execute dbt: docker compose exec dbt dbt run")
    else:
        print("⚠ INICIALIZAÇÃO CONCLUÍDA COM AVISOS")
        print("Verifique os logs acima para detalhes.")
    print("="*80)

if __name__ == "__main__":
    main()

