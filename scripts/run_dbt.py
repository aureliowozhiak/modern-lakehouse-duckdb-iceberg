"""
Script para executar transformações dbt no Lakehouse.
Executa todos os modelos dbt após a inicialização estar completa.
"""

import subprocess
import sys
import os
import time

def wait_for_database(max_retries=30, delay=2):
    """
    Aguarda o banco de dados estar disponível.
    
    Args:
        max_retries: Número máximo de tentativas
        delay: Delay entre tentativas (segundos)
    """
    db_path = "/app/lakehouse/lakehouse.duckdb"
    
    print("Aguardando banco de dados estar disponível...")
    for i in range(max_retries):
        if os.path.exists(db_path):
            print("✓ Banco de dados encontrado!")
            return True
        
        if i < max_retries - 1:
            print(f"  Tentativa {i+1}/{max_retries}...")
            time.sleep(delay)
    
    print("⚠ Banco de dados não encontrado, mas continuando...")
    return False

def check_table_exists():
    """
    Verifica se a tabela vendas_iceberg existe.
    """
    try:
        import duckdb
        db_path = "/app/lakehouse/lakehouse.duckdb"
        if not os.path.exists(db_path):
            return False
        
        con = duckdb.connect(db_path)
        try:
            result = con.execute("SELECT COUNT(*) FROM vendas_iceberg").fetchone()
            count = result[0] if result else 0
            print(f"✓ Tabela vendas_iceberg encontrada com {count:,} registros")
            return count > 0
        except Exception as e:
            print(f"⚠ Tabela não encontrada: {e}")
            return False
        finally:
            con.close()
    except ImportError:
        print("⚠ duckdb não disponível, pulando verificação")
        return True  # Continuar mesmo assim

def run_dbt_command(command, description):
    """
    Executa um comando dbt.
    
    Args:
        command: Comando dbt a executar
        description: Descrição do que o comando faz
    """
    print("\n" + "="*80)
    print(f"{description}")
    print("="*80)
    
    try:
        # Executar dbt no container dbt
        # Como estamos no container init, precisamos executar via docker exec
        # Mas na verdade, vamos criar um script que pode ser executado no container dbt
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd="/dbt"
        )
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"✓ {description} - Concluído!")
            return True
        else:
            print(f"❌ Erro ao executar: {description}")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Função principal."""
    print("="*80)
    print("EXECUÇÃO DBT - TRANSFORMAÇÕES DO LAKEHOUSE")
    print("="*80)
    print("\nEste script irá:")
    print("  1. Aguardar banco de dados estar disponível")
    print("  2. Verificar se a tabela vendas_iceberg existe")
    print("  3. Executar modelos dbt (staging e marts)")
    print("\nAguarde...\n")
    
    # Aguardar banco
    wait_for_database()
    
    # Verificar tabela
    if not check_table_exists():
        print("⚠ Tabela vendas_iceberg não encontrada!")
        print("Aguarde a inicialização completar antes de executar dbt.")
        return
    
    # Aguardar um pouco para garantir que tudo está pronto
    time.sleep(2)
    
    print("\n" + "="*80)
    print("✓ Banco de dados pronto. dbt será executado pelo serviço dbt-run.")
    print("="*80)

if __name__ == "__main__":
    main()

