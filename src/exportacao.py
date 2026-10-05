"""Fase 2: executa as consultas de sql/03_consultas.sql e exporta CSVs."""
import re

import pandas as pd
from sqlalchemy import text

from config import RAW_DIR, SQL_DIR, banner, get_engine

MARCADOR = re.compile(r"^--\s*@export\s+(\S+\.csv)\s*$", re.MULTILINE)


def extrair_consultas(conteudo: str) -> list[tuple[str, str]]:
    """Retorna [(arquivo_csv, sql)] a partir dos marcadores '-- @export'."""
    partes = MARCADOR.split(conteudo)
    # partes = [preambulo, arq1, sql1, arq2, sql2, ...]
    return [
        (partes[i], partes[i + 1].strip())
        for i in range(1, len(partes), 2)
    ]


def executar() -> None:
    conteudo = (SQL_DIR / "03_consultas.sql").read_text(encoding="utf-8")
    consultas = extrair_consultas(conteudo)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    engine = get_engine()
    with engine.connect() as conn:
        for arquivo, sql in consultas:
            df = pd.read_sql(text(sql), con=conn)
            destino = RAW_DIR / arquivo
            df.to_csv(destino, index=False, encoding="utf-8")
            print(f"[OK] {arquivo}: {len(df)} linhas -> {destino}")
    engine.dispose()

    banner(f"Fase 2 concluida: {len(consultas)} consultas exportadas.")


if __name__ == "__main__":
    executar()

