"""Ponto de entrada: executa o pipeline completo.

Uso (a partir da raiz do projeto):
    python src/run_etl.py
"""
import importlib
import sys
import time
from pathlib import Path

# Garante que os modulos de src/ sejam encontrados mesmo com
# "python -m src.run_etl" (executado a partir da raiz do projeto).
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Modulos iniciados por numero nao podem ser importados com "import";
# por isso usamos importlib.import_module com o nome em string.
ETAPAS = [
    ("Fase 0 - Banco e tabelas", "setup_db"),
    ("Fase 1 - Carga Raw", "carga_raw"),
    ("Fase 2 - Consultas e exportacao CSV", "exportacao"),
    ("Fase 2/3 - Leitura e inspecao no Pandas", "01_leitura_dados"),
    ("Fase 3 - ETL e camada tratada", "02_etl_vendas"),
    ("Fase 4 - Estatistica e respostas", "03_estatistica"),
]


def main() -> None:
    inicio = time.time()
    for i, (nome, modulo) in enumerate(ETAPAS, start=1):
        print(f"\n{'#' * 70}\n# [{i}/{len(ETAPAS)}] {nome}\n{'#' * 70}")
        importlib.import_module(modulo).executar()
    print(f"\nPipeline concluido em {time.time() - inicio:.1f}s")



if __name__ == "__main__":
    main()

