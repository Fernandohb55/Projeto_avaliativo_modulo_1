"""Fase 3: limpeza, tipagem, nulos, duplicidades e colunas derivadas."""
import numpy as np
import pandas as pd
from sqlalchemy import text

from config import (
    CSV_TRATADO,
    DIAS_SEMANA,
    PROCESSED_DIR,
    banner,
    get_engine,
)
from dicionario import gerar_dicionario

# raw (snake_case) -> nome do dicionario de dados
MAPA_COLUNAS = {
    "invoice_id": "id_venda",
    "branch": "Filial",
    "city": "Cidade",
    "customer_type": "tipo_cliente",
    "gender": "Gênero",
    "product_line": "linha_produto",
    "unit_price": "preco_unitario",
    "quantity": "Quantidade",
    "tax_5pct": "Imposto",
    "sales": "valor_total",
    "date": "data_venda",
    "time": "hora_venda",
    "payment": "forma_pagamento",
    "cogs": "custo_mercadoria",
    "gross_margin_percentage": "margem_percentual",
    "gross_income": "receita_bruta",
    "rating": "Avaliação",
}
TEXTO = [
    "id_venda", "Filial", "Cidade", "tipo_cliente", "Gênero",
    "linha_produto", "forma_pagamento", "data_venda", "hora_venda",
]
NUMERICAS = [
    "preco_unitario", "Imposto", "valor_total", "custo_mercadoria",
    "margem_percentual", "receita_bruta", "Avaliação",
]
OBRIGATORIAS = [
    "id_venda", "Filial", "Cidade", "linha_produto", "preco_unitario",
    "Quantidade", "valor_total", "data_venda", "forma_pagamento",
]
OPCIONAIS_TEXTO = ["tipo_cliente", "Gênero"]
DERIVADAS = ["dia_semana", "mes", "periodo_dia", "valor_conferido"]
COLUNAS_FINAIS = list(MAPA_COLUNAS.values()) + DERIVADAS
TABELA_TRATADA = "vendas_tratadas"


# ---------------------------------------------------------------- extrair
def extrair() -> pd.DataFrame:
    """Le a camada Raw (tudo texto) do PostgreSQL."""
    colunas = ", ".join(MAPA_COLUNAS)
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(
            text(f"SELECT {colunas} FROM raw_vendas ORDER BY invoice_id"),
            con=conn,
        )
    engine.dispose()
    print(f"Registros lidos de raw_vendas: {len(df)}")
    return df.rename(columns=MAPA_COLUNAS)


# ------------------------------------------------------------------ limpar
def limpar_texto(df: pd.DataFrame) -> pd.DataFrame:
    """Remove espacos extras e transforma vazios em nulo."""
    for col in TEXTO:
        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .replace("", pd.NA)
        )
    return df


def _parse_datetime(serie: pd.Series, formato: str) -> pd.Series:
    """Tenta o formato esperado e cai para inferencia por elemento."""
    convertido = pd.to_datetime(serie, format=formato, errors="coerce")
    if convertido.isna().any():
        alternativa = pd.to_datetime(serie, format="mixed", errors="coerce")
        convertido = convertido.fillna(alternativa)
    return convertido


def converter_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """Casting: numericos, inteiro, data e hora."""
    print("\n--- Conversao de tipos ---")
    for col in NUMERICAS + ["Quantidade"]:
        antes = df[col].notna().sum()
        df[col] = pd.to_numeric(df[col], errors="coerce")
        perdidos = antes - df[col].notna().sum()
        if perdidos:
            print(f"{col}: {perdidos} valor(es) invalido(s) -> nulo")

    # Quantidade precisa ser inteira: fracionados viram nulo
    fracionados = df["Quantidade"].notna() & (df["Quantidade"] % 1 != 0)
    if fracionados.any():
        print(f"Quantidade fracionada -> nulo: {fracionados.sum()}")
        df.loc[fracionados, "Quantidade"] = np.nan
    df["Quantidade"] = df["Quantidade"].astype("Int64")

    df["data_venda"] = _parse_datetime(df["data_venda"], "%m/%d/%Y")
    df["hora_venda"] = _parse_datetime(df["hora_venda"], "%H:%M")
    print("Tipos convertidos com sucesso.")
    return df


# ------------------------------------------------------------------- nulos
def tratar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    print("\n--- Valores ausentes ---")
    nulos = df.isna().sum()
    print(
        nulos[nulos > 0].to_string()
        if nulos.sum() > 0
        else "Nenhum valor ausente."
    )

    for col in OPCIONAIS_TEXTO:
        df[col] = df[col].fillna("Não informado")

    antes = len(df)
    df = df.dropna(subset=OBRIGATORIAS)
    print(f"Linhas removidas por nulo em campo obrigatorio: "
          f"{antes - len(df)}")
    return df


# ------------------------------------------------------------- duplicidade
def remover_duplicidades(df: pd.DataFrame) -> pd.DataFrame:
    print("\n--- Duplicidades ---")
    antes = len(df)
    df = df.drop_duplicates()
    print(f"Linhas totalmente duplicadas removidas: {antes - len(df)}")

    antes = len(df)
    df = df.drop_duplicates(subset="id_venda", keep="first")
    print(f"IDs de venda repetidos removidos: {antes - len(df)}")
    return df


# ------------------------------------------------------------------ regras
def validar_regras(df: pd.DataFrame) -> pd.DataFrame:
    """Remove registros que violariam os CHECKs do banco."""
    print("\n--- Regras de negocio (casos limitrofes) ---")

    def valido(col, cond):
        return cond(df[col]) | df[col].isna()

    regras = {
        "preco_unitario >= 0": valido("preco_unitario", lambda s: s >= 0),
        "Quantidade > 0": valido("Quantidade", lambda s: s > 0),
        "Imposto >= 0": valido("Imposto", lambda s: s >= 0),
        "valor_total >= 0": valido("valor_total", lambda s: s >= 0),
        "custo_mercadoria >= 0": valido(
            "custo_mercadoria", lambda s: s >= 0),
        "receita_bruta >= 0": valido("receita_bruta", lambda s: s >= 0),
        "Avaliação entre 0 e 10": valido(
            "Avaliação", lambda s: s.between(0, 10)),
    }
    mascara = pd.Series(True, index=df.index)
    for nome, ok in regras.items():
        invalidos = (~ok).sum()
        print(f"{nome}: {invalidos} violacao(oes)")
        mascara &= ok
    print(f"Linhas removidas por regras: {(~mascara).sum()}")
    return df[mascara].copy()


# ---------------------------------------------------------------- derivadas
def criar_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    """Feature engineering: dia_semana, mes, periodo_dia, valor_conferido."""
    df["dia_semana"] = df["data_venda"].dt.weekday.map(
        lambda i: DIAS_SEMANA[i]
    )
    df["mes"] = df["data_venda"].dt.month

    hora = df["hora_venda"].dt.hour
    df["periodo_dia"] = np.select(
        [hora.isna(), hora < 12, hora < 18],
        ["Não informado", "Manhã", "Tarde"],
        default="Noite",
    )

    esperado = (
        df["Quantidade"].astype("float64") * df["preco_unitario"]
        + df["Imposto"]
    )
    df["valor_conferido"] = ((esperado - df["valor_total"]).abs() <= 0.02)
    nao_conf = (~df["valor_conferido"]).sum()
    print(f"\nVendas com valor_total divergente do calculado: {nao_conf}")
    return df


# ------------------------------------------------------------------ salvar
def finalizar(df: pd.DataFrame) -> pd.DataFrame:
    """Arredonda para 2 casas (NUMERIC x,2) e converte data/hora."""
    for col in NUMERICAS:
        df[col] = df[col].round(2)
    df["data_venda"] = df["data_venda"].dt.date
    df["hora_venda"] = df["hora_venda"].dt.time
    for col in df.select_dtypes("string").columns:
        df[col] = df[col].astype(object)
    return df[COLUNAS_FINAIS].reset_index(drop=True)


def salvar_csv(df: pd.DataFrame) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV_TRATADO, index=False, encoding="utf-8")
    gerar_dicionario(PROCESSED_DIR)
    print(f"\nBase tratada: {CSV_TRATADO}")
    print(f"Dicionario de dados: {PROCESSED_DIR / 'dicionario_dados.csv'}")


def carregar_banco(df: pd.DataFrame) -> None:
    # NaN/NaT -> None para virar NULL no PostgreSQL
    carga = df.astype(object).where(df.notna(), None)
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {TABELA_TRATADA}"))
        carga.to_sql(
            TABELA_TRATADA,
            con=conn,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=500,
        )
    engine.dispose()


def executar() -> pd.DataFrame:
    df = extrair()
    df = limpar_texto(df)
    df = converter_tipos(df)
    df = tratar_nulos(df)
    df = remover_duplicidades(df)
    df = validar_regras(df)
    df = criar_derivadas(df)
    df = finalizar(df)

    salvar_csv(df)
    carregar_banco(df)
    banner(
        "Fase 3 concluida: camada tratada gerada.\n"
        f"Registros em {TABELA_TRATADA}: {len(df)}"
    )
    return df


if __name__ == "__main__":
    executar()

