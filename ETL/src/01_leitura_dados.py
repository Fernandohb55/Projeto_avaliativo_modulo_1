import pandas as pd

# Caminho para o ficheiro de dados (ajuste se necessário)
caminho_csv = "dados/supermarket_sales.csv"

# Leitura inicial dos dados
df = pd.read_csv(caminho_csv)

print("--- Informações Estruturais do DataFrame ---")
print(df.info())

print("\n--- Primeiras Linhas ---")
print(df.head())

print("\n--- Verificação de Valores Nulos ---")
print(df.isnull().sum())