"""Configuracoes centrais: caminhos, credenciais e engines."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ---------- Banco de dados ----------
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_ADMIN = os.getenv("DB_ADMIN", "postgres")
DB_NAME = os.getenv("DB_NAME", "supermercado")

# ---------- Caminhos ----------
SQL_DIR = BASE_DIR / "sql"
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RESULTADOS_DIR = BASE_DIR / "resultados"
GRAFICOS_DIR = RESULTADOS_DIR / "graficos"

CSV_ORIGEM = RAW_DIR / os.getenv("CSV_NOME", "SuperMarket Analysis.csv")
CSV_EXPORTADO = RAW_DIR / "export_raw_vendas.csv"
CSV_TRATADO = PROCESSED_DIR / "vendas_tratadas.csv"

# Indice = datetime.weekday() (segunda = 0)
DIAS_SEMANA = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo",
]


def _engine(database: str):
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=database,
    )
    return create_engine(url)


def get_engine_admin():
    """Engine do banco padrao (usada so para criar o banco)."""
    return _engine(DB_ADMIN)


def get_engine():
    """Engine do banco do projeto."""
    return _engine(DB_NAME)


def banner(msg: str) -> None:
    """Imprime uma mensagem delimitada por linhas."""
    largura = max(len(linha) for linha in msg.split("\n"))
    barra = "=" * largura
    print(f"{barra}\n{msg}\n{barra}")

