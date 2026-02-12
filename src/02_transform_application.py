import os

import numpy as np
import pandas as pd

from src.config import BRONZE_PATH, SILVER_PATH

def save_atomic_parquet(df, filepath):
    """Garante integridade na escrita do arquivo (Idempotência)."""
    temp_path = filepath + ".tmp"
    try:
        df.to_parquet(temp_path, index=False)
        os.replace(temp_path, filepath)
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

def process_application_data():
    print("Iniciando Higienização da Tabela Application...")
    os.makedirs(SILVER_PATH, exist_ok=True)

    # 2. Carga Unificada (Train + Test)
    # Motivo: Garantir tratamento idêntico de categorias e nulos
    print("Lendo camada Bronze...")
    df_train = pd.read_parquet(os.path.join(BRONZE_PATH, "application_train.parquet"))
    df_test = pd.read_parquet(os.path.join(BRONZE_PATH, "application_test.parquet"))
    
    df_train['is_train'] = True
    df_test['is_train'] = False
    
    # Concatena para processamento em lote
    df = pd.concat([df_train, df_test], ignore_index=True)
    
    # ==============================================================================
    # LIMPEZA E CORREÇÃO
    # ==============================================================================
    
    # Integridade de Linhas
    original_len = len(df)
    df = df.drop_duplicates(subset=['sk_id_curr'], keep='first')
    if len(df) < original_len:
        print(f"Removidas {original_len - len(df)} duplicatas de SK_ID_CURR")

    # Tratamento da Anomalia Identificada
    print(f"Tratando anomalia '365243' em DAYS_EMPLOYED...")
    anomalia_mask = df['days_employed'] == 365243
    df['days_employed_anom'] = anomalia_mask.astype(int)
    df['days_employed'] = df['days_employed'].replace(365243, np.nan)
    
    # Correção Temporal (Negativo -> Positivo/Anos)
    time_cols = ['days_birth', 'days_employed', 'days_registration', 'days_id_publish']
    for col in time_cols:
        new_col_name = col.replace('days_', 'years_')
        df[new_col_name] = df[col] / -365.25

    # ==============================================================================
    # FEATURE ENGINEERING
    # ==============================================================================
    
    # Ratios Financeiros (Padrão de Mercado)
    # A EDA mostrou outliers de renda. O Ratio normaliza isso.
    df['ratio_credit_income'] = df['amt_credit'] / df['amt_income_total']
    df['ratio_annuity_income'] = df['amt_annuity'] / df['amt_income_total']
    df['ratio_credit_annuity'] = df['amt_credit'] / df['amt_annuity'] # Prazo estimado
    
    #Flag de Dados de Moradia
    # Agrupa colunas de moradia
    cols_housing = [c for c in df.columns if ('_avg' in c or '_mode' in c or '_medi' in c) and 'ext_source' not in c]
    df['flag_has_housing_info'] = df[cols_housing].notnull().any(axis=1).astype(int)
    
    # Consolidação de Fontes Externas (Top Correlações Negativas)
    # Unifica o sinal de ext_source_1, 2 e 3 em uma média robusta
    df['ext_source_mean'] = df[['ext_source_1', 'ext_source_2', 'ext_source_3']].mean(axis=1)

    # ==============================================================================
    # OTIMIZAÇÃO E SALVAMENTO
    # ==============================================================================
    
    # Tratamento de Categorias
    # Preenche nulos em texto com 'XNA' (Not Available)
    cat_cols = df.select_dtypes(include=['object', 'string']).columns
    for col in cat_cols:
        df[col] = df[col].fillna('XNA').astype('category')

    # Separação Final
    print("Salvando Camada Silver...")
    
    df_train_silver = df[df['is_train'] == True].drop(columns=['is_train'])
    
    # Garante que teste não tenha target nem colunas de controle
    cols_drop_test = ['is_train', 'target'] if 'target' in df.columns else ['is_train']
    df_test_silver = df[df['is_train'] == False].drop(columns=cols_drop_test, errors='ignore')

    try:
        save_atomic_parquet(df_train_silver, os.path.join(SILVER_PATH, "fact_application_train.parquet"))
        save_atomic_parquet(df_test_silver, os.path.join(SILVER_PATH, "fact_application_test.parquet"))
        print(f"Sucesso! Train: {df_train_silver.shape} | Test: {df_test_silver.shape}")
        print(f"      (Features de Moradia preservadas via flag: 'flag_has_housing_info')")
        print(f"      (Anomalia de emprego tratada e preservada em: 'days_employed_anom')")
    except Exception as e:
        print(f"Erro crítico ao salvar: {e}")

if __name__ == "__main__":
    process_application_data()