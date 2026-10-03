import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Carregar variáveis de ambiente do ficheiro .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def configurar_data_warehouse():
    print("==========================================")
    print(" CONFIGURAÇÃO DO DATA WAREHOUSE (DW)")
    print("==========================================")
    
    with engine.begin() as conn:
        # 1. Criar os Schemas da Arquitetura Medallion
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold;"))
        print("[OK] Schemas criados/verificados: bronze, silver, gold.")
        
        # 2. Opcional: Garantir extensões úteis no PostgreSQL se necessário
        # conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))

    print("==========================================")
    print(" DATA WAREHOUSE PRONTO A SER UTILIZADO!")
    print("==========================================")

if __name__ == "__main__":
    configurar_data_warehouse()