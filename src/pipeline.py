import time
import importlib
from datetime import datetime
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(current_dir)

# Adiciona a raiz ao sys.path se não estiver lá
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def run_full_pipeline():
    start_time = time.time()
    print(f"{'='*60}")
    print(f"INICIANDO PIPELINE DE DADOS - {datetime.now()}")
    print(f"{'='*60}")
    
    try:
        # ----------------------------------------------------------------------
        # PASSO 1: INGESTÃO (Raw -> Bronze)
        # ----------------------------------------------------------------------
        # Arquivo: src/01_ingestion.py
        print("\n[1/4] Executando Ingestão...")
        mod_ingestion = importlib.import_module("src.01_ingestion")
        
        if hasattr(mod_ingestion, 'run_ingestion'):
            mod_ingestion.run_ingestion()
        else:
            raise AttributeError("A função 'run_ingestion' não foi encontrada em src/01_ingestion.py")
        
        # ----------------------------------------------------------------------
        # PASSO 2: TRANSFORMAÇÃO FATO (Bronze -> Silver)
        # ----------------------------------------------------------------------
        # Arquivo: src/02_transform_application.py
        print("\n[2/4] Executando Transformação Application...")
        mod_app = importlib.import_module("src.02_transform_application")
        mod_app.process_application_data()
        
        # ----------------------------------------------------------------------
        # PASSO 3: TRANSFORMAÇÃO DIMENSÕES (Bronze -> Silver)
        # ----------------------------------------------------------------------
        # Arquivo: src/02b_transform_dimensions.py
        print("\n[3/4] Executando Transformação Dimensões...")
        mod_dims = importlib.import_module("src.02b_transform_dimensions")
        mod_dims.run_pipeline()
        
        # ----------------------------------------------------------------------
        # PASSO 4: CAMADA ANALÍTICA (Silver -> Gold)
        # ----------------------------------------------------------------------
        # Arquivo: src/03_analytical_layer.py
        print("\n[4/4] Construindo Camada Analítica (OBT)...")
        mod_gold = importlib.import_module("src.03_analytical_layer")
        mod_gold.build_obt()
        
        # ----------------------------------------------------------------------
        # FINALIZAÇÃO
        # ----------------------------------------------------------------------
        elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        print(f" PIPELINE CONCLUÍDO COM SUCESSO em {elapsed:.2f} segundos.")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"\n FALHA CRÍTICA NO PIPELINE: {e}")

if __name__ == "__main__":
    run_full_pipeline()