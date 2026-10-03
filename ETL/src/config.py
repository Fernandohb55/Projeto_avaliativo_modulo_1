import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()

# Obter a string de conexão do PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# Criar o engine global do SQLAlchemy para reutilização em todo o projeto
engine = create_engine(DATABASE_URL) if DATABASE_URL else None

# Caminhos base úteis para o projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")