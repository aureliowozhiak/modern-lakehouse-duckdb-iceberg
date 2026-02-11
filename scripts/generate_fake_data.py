"""
Script para gerar dados fake para o Lakehouse.
Gera dados de vendas simulados com informações de produtos, clientes e transações.
"""

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Configuração
fake = Faker('pt_BR')
Faker.seed(42)
random.seed(42)

def generate_sales_data(num_records=1000):
    """
    Gera dados simulados de vendas.
    
    Args:
        num_records: Número de registros a gerar
        
    Returns:
        DataFrame com dados de vendas
    """
    print(f"Gerando {num_records} registros de vendas...")
    
    data = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    # Produtos pré-definidos
    produtos = [
        {"id": 1, "nome": "Notebook Dell", "categoria": "Eletrônicos", "preco_base": 3500.00},
        {"id": 2, "nome": "Mouse Logitech", "categoria": "Periféricos", "preco_base": 150.00},
        {"id": 3, "nome": "Teclado Mecânico", "categoria": "Periféricos", "preco_base": 450.00},
        {"id": 4, "nome": "Monitor 27 polegadas", "categoria": "Eletrônicos", "preco_base": 1200.00},
        {"id": 5, "nome": "Webcam HD", "categoria": "Periféricos", "preco_base": 300.00},
        {"id": 6, "nome": "SSD 1TB", "categoria": "Armazenamento", "preco_base": 500.00},
        {"id": 7, "nome": "Memória RAM 16GB", "categoria": "Componentes", "preco_base": 400.00},
        {"id": 8, "nome": "Placa de Vídeo RTX 3060", "categoria": "Componentes", "preco_base": 2500.00},
        {"id": 9, "nome": "Headset Gamer", "categoria": "Periféricos", "preco_base": 350.00},
        {"id": 10, "nome": "Tablet Samsung", "categoria": "Eletrônicos", "preco_base": 1800.00},
    ]
    
    for i in range(num_records):
        produto = random.choice(produtos)
        data_venda = fake.date_between(start_date=start_date, end_date=end_date)
        hora_venda = fake.time()
        timestamp_venda = datetime.combine(data_venda, datetime.strptime(hora_venda, "%H:%M:%S").time())
        
        # Variação de preço (±10%)
        variacao_preco = random.uniform(-0.10, 0.10)
        preco_venda = produto["preco_base"] * (1 + variacao_preco)
        
        # Quantidade (1-5 unidades)
        quantidade = random.randint(1, 5)
        valor_total = preco_venda * quantidade
        
        # Desconto (0-20%)
        desconto_percentual = random.uniform(0, 0.20) if random.random() > 0.3 else 0
        valor_desconto = valor_total * desconto_percentual
        valor_final = valor_total - valor_desconto
        
        # Cliente
        cliente_id = random.randint(1000, 9999)
        cliente_nome = fake.name()
        cliente_email = fake.email()
        cliente_cidade = fake.city()
        cliente_estado = fake.state_abbr()
        
        # Canal de venda
        canal = random.choice(["Online", "Loja Física", "Marketplace", "Telefone"])
        
        # Status
        status = random.choice(["Concluída", "Concluída", "Concluída", "Cancelada", "Pendente"])
        
        record = {
            "venda_id": f"V{10000 + i:06d}",
            "data_venda": timestamp_venda.strftime("%Y-%m-%d"),
            "timestamp_venda": timestamp_venda.isoformat(),
            "produto_id": produto["id"],
            "produto_nome": produto["nome"],
            "categoria": produto["categoria"],
            "preco_unitario": round(preco_venda, 2),
            "quantidade": quantidade,
            "valor_total": round(valor_total, 2),
            "desconto_percentual": round(desconto_percentual * 100, 2),
            "valor_desconto": round(valor_desconto, 2),
            "valor_final": round(valor_final, 2),
            "cliente_id": cliente_id,
            "cliente_nome": cliente_nome,
            "cliente_email": cliente_email,
            "cliente_cidade": cliente_cidade,
            "cliente_estado": cliente_estado,
            "canal_venda": canal,
            "status": status
        }
        
        data.append(record)
    
    df = pd.DataFrame(data)
    print(f"✓ {len(df)} registros gerados com sucesso!")
    print(f"\nEstatísticas:")
    print(f"  - Período: {df['data_venda'].min()} até {df['data_venda'].max()}")
    print(f"  - Valor total: R$ {df['valor_final'].sum():,.2f}")
    print(f"  - Média por venda: R$ {df['valor_final'].mean():,.2f}")
    print(f"  - Categorias: {df['categoria'].nunique()}")
    print(f"  - Clientes únicos: {df['cliente_id'].nunique()}")
    
    return df

def save_to_parquet(df, output_path):
    """
    Salva DataFrame em formato Parquet.
    
    Args:
        df: DataFrame a ser salvo
        output_path: Caminho do arquivo de saída
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path, index=False, engine='pyarrow')
    print(f"\n✓ Dados salvos em: {output_path}")
    print(f"  Tamanho do arquivo: {os.path.getsize(output_path) / 1024:.2f} KB")

if __name__ == "__main__":
    # Gerar dados
    df = generate_sales_data(num_records=5000)
    
    # Salvar em Parquet
    output_dir = "/app/data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "vendas_raw.parquet")
    save_to_parquet(df, output_path)
    
    # Mostrar amostra
    print("\n" + "="*80)
    print("Amostra dos dados gerados:")
    print("="*80)
    print(df.head(10).to_string())

