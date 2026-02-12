"""
Configuração centralizada do pipeline.
Carrega variáveis de ambiente uma única vez e expõe os caminhos das camadas.
"""
import os

from dotenv import load_dotenv

load_dotenv()

# Caminhos das camadas (com valores padrão quando aplicável)
RAW_PATH = os.getenv("RAW_DATA_PATH")
BRONZE_PATH = os.getenv("BRONZE_DATA_PATH", "data/bronze")
SILVER_PATH = os.getenv("SILVER_DATA_PATH", "data/silver")
GOLD_PATH = os.getenv("GOLD_DATA_PATH", "data/gold")


def get_ingestion_paths():
    """Retorna (raw_path, bronze_path) para ingestão. Exige RAW e BRONZE configurados."""
    if not RAW_PATH or not BRONZE_PATH:
        raise ValueError(
            "Variáveis de ambiente não configuradas. "
            "Defina RAW_DATA_PATH e BRONZE_DATA_PATH no .env (veja .env.example)."
        )
    return RAW_PATH, BRONZE_PATH
