"""Fase 0: cria o banco e as tabelas executando os scripts SQL."""
from sqlalchemy import text

from config import (
    DB_NAME,
    SQL_DIR,
    banner,
    get_engine,
    get_engine_admin,
)


def ler_sql(nome_arquivo: str) -> str:
    return (SQL_DIR / nome_arquivo).read_text(encoding="utf-8")


def criar_banco() -> None:
    """Executa 01_criar_banco.sql se o banco ainda nao existir."""
    engine = get_engine_admin()
    with engine.connect().execution_options(
        isolation_level="AUTOCOMMIT"
    ) as conn:
        existe = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :nome"),
            {"nome": DB_NAME},
        ).scalar()
        if existe:
            print(f"Banco '{DB_NAME}' ja existe. Nada a fazer.")
        else:
            conn.exec_driver_sql(ler_sql("01_criar_banco.sql"))
            print(f"Banco '{DB_NAME}' criado com sucesso.")
    engine.dispose()


def criar_tabelas() -> None:
    """Executa 02_criar_tabelas.sql (idempotente)."""
    engine = get_engine()
    with engine.begin() as conn:
        conn.exec_driver_sql(ler_sql("02_criar_tabelas.sql"))
    engine.dispose()
    print("Tabelas raw_vendas e vendas_tratadas verificadas/criadas.")


def executar() -> None:
    criar_banco()
    criar_tabelas()
    banner("Fase 0 concluida: banco e tabelas prontos.")


if __name__ == "__main__":
    executar()

