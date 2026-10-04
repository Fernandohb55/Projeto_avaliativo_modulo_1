"""Fase 2/3: leitura do CSV exportado e inspecao inicial (EDA) no Pandas."""
import io

import pandas as pd

from config import CSV_EXPORTADO, RESULTADOS_DIR, banner

COLUNAS_CATEGORICAS = [
    "branch",
    "city",
    "customer_type",
    "gender",
    "product_line",
    "payment",
]
COLUNAS_NUMERICAS = [
    "unit_price",
    "quantity",
    "tax_5pct",
    "sales",
    "cogs",
    "gross_income",
    "rating",
]


def inspecionar(df: pd.DataFrame) -> list[str]:
    """Gera o relatorio de inspecao como lista de linhas de texto."""
    out: list[str] = []
    add = out.append

    add(f"Dimensoes: {df.shape[0]} linhas x {df.shape[1]} colunas")

    add("\n--- 1. Tipos de dados (inferidos pelo Pandas) ---")
    buf = io.StringIO()
    df.info(buf=buf)
    add(buf.getvalue())

    add("--- 2. Valores nulos ---")
    nulos = df.isnull().sum()
    add(
        nulos[nulos > 0].to_string()
        if nulos.sum() > 0
        else "Nenhum valor nulo encontrado."
    )

    add("\n--- 3. Duplicidades ---")
    add(f"Linhas totalmente duplicadas: {df.duplicated().sum()}")
    add(f"Invoice IDs repetidos: {df['invoice_id'].duplicated().sum()}")

    add("\n--- 4. Cardinalidade das categorias ---")
    for col in COLUNAS_CATEGORICAS:
        add(f"{col}: {sorted(df[col].dropna().unique().tolist())}")

    add("\n--- 5. Estatisticas descritivas (numericas) ---")
    add(df[COLUNAS_NUMERICAS].describe().round(2).to_string())

    add("\n--- 6. Inconsistencias ---")
    add(f"quantity <= 0: {(df['quantity'] <= 0).sum()}")
    add(f"unit_price < 0: {(df['unit_price'] < 0).sum()}")
    add(f"rating fora de 0-10: {(~df['rating'].between(0, 10)).sum()}")
    dif = (df["cogs"] + df["tax_5pct"] - df["sales"]).abs()
    add(f"sales != cogs + tax (tolerancia 0,01): {(dif > 0.01).sum()}")

    add("\n--- 7. Amostra ---")
    add(df.head(3).to_string())
    return out


def executar() -> pd.DataFrame:
    if not CSV_EXPORTADO.exists():
        raise FileNotFoundError(
            f"{CSV_EXPORTADO} nao existe. Execute antes src/exportacao.py."
        )
    df = pd.read_csv(CSV_EXPORTADO)

    banner(f"Inspecao inicial: {CSV_EXPORTADO.name}")
    linhas = inspecionar(df)
    texto = "\n".join(linhas)
    print(texto)

    RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTADOS_DIR / "inspecao_inicial.txt").write_text(
        texto, encoding="utf-8"
    )
    banner("Inspecao concluida (relatorio em resultados/inspecao_inicial.txt)")
    return df


if __name__ == "__main__":
    executar()

