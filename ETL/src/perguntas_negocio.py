import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar variáveis de ambiente e conexão
load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def executar_todas_as_perguntas():
    print("==================================================")
    print(" RELATÓRIO COMPLETO: AS 8 PERGUNTAS DE NEGÓCIO")
    print("==================================================")
    
    # Carregar dados limpos da camada Silver
    try:
        df = pd.read_sql("SELECT * FROM silver.supermarket_clean", con=engine)
    except Exception as e:
        print(f"[Erro] Falha ao carregar dados da camada Silver: {e}")
        return

    # ----------------------------------------------------
    # BLOCO 1: Pergunta 1
    # ----------------------------------------------------
    print("\n--- [Bloco 1] Pergunta 1: Vendas Totais por Linha de Produto ---")
    bloco1 = df.groupby("product_line")["total"].sum().reset_index().sort_values(by="total", ascending=False)
    print(bloco1.to_string(index=False))

    # ----------------------------------------------------
    # BLOCO 2: Pergunta 2
    # ----------------------------------------------------
    print("\n--- [Bloco 2] Pergunta 2: Receita por Tipo de Cliente ---")
    bloco2 = df.groupby("customer_type")["total"].sum().reset_index().sort_values(by="total", ascending=False)
    print(bloco2.to_string(index=False))

    # ----------------------------------------------------
    # BLOCO 3: Pergunta 3
    # ----------------------------------------------------
    print("\n--- [Bloco 3] Pergunta 3: Métodos de Pagamento mais Utilizados ---")
    bloco3 = df["payment"].value_counts().reset_index()
    bloco3.columns = ["metodo_pagamento", "frequencia"]
    print(bloco3.to_string(index=False))

    # ----------------------------------------------------
    # BLOCO 4: Pergunta 4
    # ----------------------------------------------------
    print("\n--- [Bloco 4] Pergunta 4: Desempenho de Vendas por Filial (Branch) ---")
    bloco4 = df.groupby("branch")["total"].sum().reset_index().sort_values(by="total", ascending=False)
    print(bloco4.to_string(index=False))

    # ----------------------------------------------------
    # BLOCO 5: Pergunta 5
    # ----------------------------------------------------
    print("\n--- [Bloco 5] Pergunta 5: Avaliação Média (Rating) por Linha de Produto ---")
    bloco5 = df.groupby("product_line")["rating"].mean().reset_index().sort_values(by="rating", ascending=False)
    print(bloco5.to_string(index=False))

    # ----------------------------------------------------
    # BLOCO 6: Pergunta 6
    # ----------------------------------------------------
    print("\n--- [Bloco 6] Pergunta 6: Custo do CMV (COGS) vs Receita Total ---")
    bloco6 = df.groupby("product_line")[["total", "cogs"]].sum().reset_index()
    print(bloco6.to_string(index=False))

    # ----------------------------------------------------
    # BLOCO 7: Pergunta 7
    # ----------------------------------------------------
    print("\n--- [Bloco 7] Pergunta 7: Volume de Vendas por Género de Cliente ---")
    bloco7 = df.groupby("gender")["total"].sum().reset_index().sort_values(by="total", ascending=False)
    print(bloco7.to_string(index=False))

    # ----------------------------------------------------
    # BLOCO 8: Pergunta 8
    # ----------------------------------------------------
    print("\n--- [Bloco 8] Pergunta 8: Transações por Horário/Período ---")
    # Exemplo simples com base na coluna de hora
    bloco8 = df.groupby("time")["invoice_id"].count().reset_index().head(10)
    print(bloco8.to_string(index=False))

    print("==================================================")
    print(" TODAS AS 8 PERGUNTAS PROCESSADAS COM SUCESSO!")
    print("==================================================")

if __name__ == "__main__":
    executar_todas_as_perguntas()