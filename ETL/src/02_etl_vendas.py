import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# Carregar variáveis de ambiente
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Ler dados brutos
df = pd.read_csv("dados/supermarket_sales.csv")

# Transformações e Limpeza (Silver)
df["Date"] = pd.to_datetime(df["Date"])
df.dropna(inplace=True)

# Normalizar nomes de colunas para minúsculas (boas práticas em SQL)
df.columns = [col.lower().replace(" ", "_") for col in df.columns]

# Enviar para a camada Silver no PostgreSQL
df.to_sql(
    name="supermarket_clean",
    con=engine,
    schema="silver",
    if_exists="replace",
    index=False,
)

print("ETL executado com sucesso: dados tratados guardados na camada Silver!")