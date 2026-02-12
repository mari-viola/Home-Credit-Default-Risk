"""
Configuração compartilhada do pytest.
Garante que o diretório raiz do projeto esteja no PYTHONPATH
e que variáveis de ambiente mínimas existam para carregar módulos do pipeline.
"""
import sys
from pathlib import Path

# Raiz do projeto (pasta que contém src/ e tests/)
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Valores padrão para testes que importam 01_ingestion (evita falha de get_ingestion_paths)
import os
os.environ.setdefault("RAW_DATA_PATH", "data/raw")
os.environ.setdefault("BRONZE_DATA_PATH", "data/bronze")
