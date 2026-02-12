import os

import pandas as pd

from src.config import GOLD_PATH, SILVER_PATH

def save_atomic_parquet(df, filename):
    filepath = os.path.join(GOLD_PATH, filename)
    temp_path = filepath + ".tmp"
    try:
        df.to_parquet(temp_path, index=False)
        os.replace(temp_path, filepath)
        print(f"Salvo: {filename} | Formato: {df.shape}")
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"Erro ao salvar {filename}: {e}")

def build_obt():
    print("[Fase 3] Iniciando Construção da Camada Analítica (Gold / OBT)...")
    os.makedirs(GOLD_PATH, exist_ok=True)

    # 1. Carregando Dimensões
    print("Carregando Dimensões (Silver)...")
    dim_bureau = pd.read_parquet(os.path.join(SILVER_PATH, "dim_bureau.parquet"))
    dim_prev = pd.read_parquet(os.path.join(SILVER_PATH, "dim_previous_app.parquet"))
    dim_inst = pd.read_parquet(os.path.join(SILVER_PATH, "dim_installments.parquet"))
    dim_cc = pd.read_parquet(os.path.join(SILVER_PATH, "dim_credit_card.parquet"))
    dim_pos = pd.read_parquet(os.path.join(SILVER_PATH, "dim_pos_cash.parquet"))

    # Lista de dimensões para o loop de JOIN
    dimensions = [dim_bureau, dim_prev, dim_inst, dim_cc, dim_pos]

    # 2. Função interna para fazer o JOIN garantindo a integridade
    def merge_to_obt(fact_df, fact_name):
        print(f"\n Montando OBT para: {fact_name}...")
        obt = fact_df.copy()
        
        # Sequência de LEFT JOINs usando SK_ID_CURR
        for dim in dimensions:
            # Obtém o nome da primeira coluna (excluindo sk_id_curr) para log
            dim_prefix = dim.columns[1].split('_')[0] if len(dim.columns) > 1 else "DIM"
            print(f"      -> Fazendo JOIN com Dimensão: {dim_prefix}")
            obt = obt.merge(dim, on='sk_id_curr', how='left')
            
        return obt

    # 3. Processando Treino
    fact_train = pd.read_parquet(os.path.join(SILVER_PATH, "fact_application_train.parquet"))
    obt_train = merge_to_obt(fact_train, "Treino (Com Target)")
    save_atomic_parquet(obt_train, "analytics_credit_risk_train.parquet")

    # 4. Processar Teste
    fact_test = pd.read_parquet(os.path.join(SILVER_PATH, "fact_application_test.parquet"))
    obt_test = merge_to_obt(fact_test, "Teste (Sem Target)")
    save_atomic_parquet(obt_test, "analytics_credit_risk_test.parquet")

    print("\n Camada Ouro concluída!")

if __name__ == "__main__":
    build_obt()