import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text

# Carregar variáveis de ambiente
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def carregar_camada_bronze():
    print("--- A iniciar o carregamento da Camada Bronze ---")
    
    # 1. Garantir que o schema bronze existe no Data Warehouse
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze;"))
    
    # 2. Definir o caminho do ficheiro CSV bruto
    caminho_csv = "data/supermarket_sales.csv"
    
    if not os.path.exists(caminho_csv):
        print(f"[Erro] Ficheiro CSV não encontrado no caminho: {caminho_csv}")
        return
    
    # 3. Ler o ficheiro CSV com o Pandas
    df_raw = pd.read_csv(caminho_csv)
    
    # 4. Enviar os dados brutos para a tabela do esquema bronze
    df_raw.to_sql(
        name="supermarket_raw",
        con=engine,
        schema="bronze",
        if_exists="replace",
        index=False
    )
    
    print("Camada Bronze executada com sucesso: dados brutos guardados na tabela 'bronze.supermarket_raw'!")

if __name__ == "__main__":
    carregar_camada_bronze()