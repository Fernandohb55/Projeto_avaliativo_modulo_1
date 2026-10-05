"""Fase 1: carrega o CSV original, sem alterar o conteudo, em raw_vendas."""
import pandas as pd
from sqlalchemy import text

from config import CSV_ORIGEM, banner, get_engine

TABELA_RAW = "raw_vendas"

# Nome original no CSV -> coluna da tabela raw (so troca o formato do
# nome; os valores permanecem exatamente como no arquivo).
MAPA_COLUNAS_RAW = {
    "Invoice ID": "invoice_id",
    "Branch": "branch",
    "City": "city",
    "Customer type": "customer_type",
    "Gender": "gender",
    "Product line": "product_line",
    "Unit price": "unit_price",
    "Quantity": "quantity",
    "Tax 5%": "tax_5pct",
    "Sales": "sales",
    "Date": "date",
    "Time": "time",
    "Payment": "payment",
    "cogs": "cogs",
    "gross margin percentage": "gross_margin_percentage",
    "gross income": "gross_income",
    "Rating": "rating",
}


def ler_csv_original() -> pd.DataFrame:
    if not CSV_ORIGEM.exists():
        raise FileNotFoundError(
            f"CSV nao encontrado: {CSV_ORIGEM}\n"
            "Baixe o dataset do Kaggle e salve em data/raw/."
        )
    # dtype=str preserva exatamente o texto de cada celula
    df = pd.read_csv(CSV_ORIGEM, dtype=str)
    faltantes = set(MAPA_COLUNAS_RAW) - set(df.columns)
    if faltantes:
        raise ValueError(f"Colunas ausentes no CSV: {sorted(faltantes)}")
    return df[list(MAPA_COLUNAS_RAW)].rename(columns=MAPA_COLUNAS_RAW)


def executar() -> None:
    df = ler_csv_original()
    engine = get_engine()

    # TRUNCATE + INSERT na mesma transacao: ou carrega tudo ou nada
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {TABELA_RAW}"))
        df.to_sql(
            TABELA_RAW,
            con=conn,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=500,
        )

    with engine.connect() as conn:
        total_banco = conn.execute(
            text(f"SELECT COUNT(*) FROM {TABELA_RAW}")
        ).scalar()
    engine.dispose()

    banner(
        "Fase 1 concluida: carga Raw.\n"
        f"Linhas no CSV: {len(df)} | Linhas em {TABELA_RAW}: {total_banco}"
    )
    if total_banco != len(df):
        raise RuntimeError("Contagem do banco difere da do CSV!")


if __name__ == "__main__":
    executar()

