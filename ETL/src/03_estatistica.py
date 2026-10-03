import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

# Conexão à base de dados
load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

# Ler dados limpos da camada Silver
df = pd.read_sql("SELECT * FROM silver.supermarket_clean", con=engine)

# Estatística descritiva básica
print("--- Estatística Descritiva das Vendas ---")
print(df[["unit_price", "quantity", "total", "gross_income"]].describe())

# Agregação para resposta de negócio: Vendas por Linha de Produto
vendas_por_linha = (
    df.groupby("product_line")["total"].sum().reset_index().sort_values(by="total", ascending=False)
)

print("\n--- Resumo de Vendas por Linha de Produto ---")
print(vendas_por_linha)

# Geração do Gráfico Analítico
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

sns.barplot(
    data=vendas_por_linha,
    x="total",
    y="product_line",
    palette="Blues_r",
    hue="product_line",
    legend=False,
)

plt.title("Total de Vendas por Linha de Produto", fontsize=14, fontweight="bold")
plt.xlabel("Receita Total ($)")
plt.ylabel("Linha de Produto")
plt.tight_layout()

# Mostrar o gráfico
plt.show()