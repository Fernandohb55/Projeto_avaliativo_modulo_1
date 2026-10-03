import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text

# Carregar variáveis de ambiente
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def executar_pipeline_etl():
    print("==========================================")
    print(" INICIANDO PIPELINE ETL (MEDALLION)")
    print("==========================================")
    
    # 1. Criar schemas no Data Warehouse
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold;"))
    print("[1/4] Schemas (bronze, silver, gold) criados/verificados com sucesso.")

    # 2. Camada Bronze (Injestão de dados brutos)
    caminho_csv = "data/supermarket_sales.csv"  # Ajuste o caminho se necessário
    if not os.path.exists(caminho_csv):
        print(f"[Erro] Ficheiro CSV não encontrado no caminho: {caminho_csv}")
        return
    
    df_raw = pd.read_csv(caminho_csv)
    df_raw.to_sql(
        name="supermarket_raw",
        con=engine,
        schema="bronze",
        if_exists="replace",
        index=False
    )
    print("[2/4] Camada Bronze: Dados brutos carregados com sucesso.")

    # 3. Camada Silver (Limpeza e Tratamento)
    df_silver = df_raw.copy()
    df_silver["Date"] = pd.to_datetime(df_silver["Date"])
    df_silver.dropna(inplace=True)
    
    # Padronizar nomes de colunas para minúsculas
    df_silver.columns = [col.lower().replace(" ", "_") for col in df_silver.columns]
    
    df_silver.to_sql(
        name="supermarket_clean",
        con=engine,
        schema="silver",
        if_exists="replace",
        index=False
    )
    print("[3/4] Camada Silver: Dados limpos e transformados carregados com sucesso.")

    # 4. Camada Gold (Agregações de Negócio)
    df_gold = (
        df_silver.groupby("product_line")
        .agg(
            total_vendas=("total", "sum"),
            media_vendas=("total", "mean"),
            quantidade_total=("quantity", "sum")
        )
        .reset_index()
    )
    
    df_gold.to_sql(
        name="vendas_por_linha_produto",
        con=engine,
        schema="gold",
        if_exists="replace",
        index=False
    )
    print("[4/4] Camada Gold: Tabelas agregadas criadas com sucesso.")
    
    print("==========================================")
    print(" PIPELINE EXECUTADO COM SUCESSO A 100%!")
    print("==========================================")

if __name__ == "__main__":
    executar_pipeline_etl()