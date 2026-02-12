import os
import time

import pandas as pd

from src.config import BRONZE_PATH, RAW_PATH, get_ingestion_paths

# Validação dos paths obrigatórios para ingestão
get_ingestion_paths()

files_to_ingest = [
    'application_train.csv', 'application_test.csv', 'bureau.csv',
    'bureau_balance.csv', 'previous_application.csv', 'POS_CASH_balance.csv',
    'credit_card_balance.csv', 'installments_payments.csv'
]

def save_atomic_parquet(df, output_path):
    """
    Implementa Escrita Atômica:
    1. Salva em um arquivo temporário (.tmp).
    2. Se sucesso, renomeia para o final, substituindo o antigo atomicamente.
    Isso previne corrupção de arquivos em caso de falha no meio da escrita.
    """
    temp_path = output_path + ".tmp"
    
    try:
        # Escrita no arquivo temporário
        df.to_parquet(
            temp_path,
            engine="pyarrow",
            compression="snappy",
            index=False
        )
        
        # Operação Atômica: Substitui o arquivo final pelo temporário
        if os.path.exists(output_path):
            print(f"Substituindo arquivo existente: {os.path.basename(output_path)}")
        
        os.replace(temp_path, output_path)
        
    except Exception as e:
        # Se der erro, limpamos o .tmp
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

def process_file(file_name):
    """Lógica isolada de processamento por arquivo com validações."""
    input_path = os.path.join(RAW_PATH, file_name)
    output_name = file_name.replace('.csv', '.parquet')
    output_path = os.path.join(BRONZE_PATH, output_name)
    
    # --- Validação Prévia ---
    if not os.path.exists(input_path):
        print(f"PULADO: {file_name} não encontrado na origem.")
        return
    
    # Verifica se o arquivo não está vazio (evita criar parquets vazios)
    if os.path.getsize(input_path) == 0:
        print(f"PULADO: {file_name} está vazio.")
        return

    try:
        start_time = time.time()
        print(f"Variáveis: Lendo {file_name}...")
        
        # Leitura
        df = pd.read_csv(input_path)
        
        # Transformação leve
        df.columns = [col.lower().strip() for col in df.columns]
        
        # ---(Controlled Overwrite) ---
        save_atomic_parquet(df, output_path)
        
        elapsed = time.time() - start_time
        print(f"SUCESSO: {output_name} ({df.shape[0]} linhas) - {elapsed:.2f}s")
        
    except Exception as e:
        print(f"ERRO CRÍTICO em {file_name}: {str(e)}")

def run_ingestion():
    os.makedirs(BRONZE_PATH, exist_ok=True)
    
    print(f"Iniciando Ingestão")
    print(f"Origem: {RAW_PATH}")
    print(f"Destino: {BRONZE_PATH}")
    print("-" * 40)
    
    for file_name in files_to_ingest:
        process_file(file_name)

if __name__ == "__main__":
    run_ingestion()