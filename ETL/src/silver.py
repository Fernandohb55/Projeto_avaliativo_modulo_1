import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text

# Carregar variáveis de ambiente
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def executar_camada_silver():
    print("--- A iniciar o processamento da Camada Silver ---")
    
    # 1. Garantir que o schema silver existe no Data Warehouse
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver;"))
    
    # 2. Ler os dados brutos da camada Bronze no PostgreSQL
    try:
        df_bronze = pd.read_sql("SELECT * FROM bronze.supermarket_raw", con=engine)
    except Exception as e:
        print(f"[Erro] Não foi possível ler da camada bronze. Certifique-se de que executou o bronze.py primeiro. Detalhe: {e}")
        return
    
    # 3. Transformações e Limpeza (Silver)
    df_silver = df_bronze.copy()
    
    # Converter a coluna de data para datetime
    df_silver["Date"] = pd.to_datetime(df_silver["Date"])
    
    # Remover linhas com valores nulos, se existirem
    df_silver.dropna(inplace=True)
    
    # Padronizar os nomes das colunas para minúsculas (boas práticas em SQL)
    df_silver.columns = [col.lower().replace(" ", "_") for col in df_silver.columns]
    
    # 4. Enviar os dados limpos para a tabela do esquema silver
    df_silver.to_sql(
        name="supermarket_clean",
        con=engine,
        schema="silver",
        if_exists="replace",
        index=False
    )
    
    print("Camada Silver executada com sucesso: dados limpos guardados na tabela 'silver.supermarket_clean'!")

if __name__ == "__main__":
    executar_camada_silver()