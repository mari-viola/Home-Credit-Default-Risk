import os

import numpy as np
import pandas as pd

from src.config import BRONZE_PATH, SILVER_PATH

def save_atomic_parquet(df, filename):
    """Garante escrita segura (Idempotência)."""
    filepath = os.path.join(SILVER_PATH, filename)
    temp_path = filepath + ".tmp"
    try:
        df.to_parquet(temp_path, index=False)
        os.replace(temp_path, filepath)
        print(f"Salvo: {filename} | Formato: {df.shape}")
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"Erro ao salvar {filename}: {e}")

# ==============================================================================
# BUREAU & BUREAU BALANCE
# ==============================================================================
def process_bureau():
    print("Processando: Bureau e Bureau Balance...")
    bureau = pd.read_parquet(os.path.join(BRONZE_PATH, "bureau.parquet"))
    balance = pd.read_parquet(os.path.join(BRONZE_PATH, "bureau_balance.parquet"))

    # Agrega Bureau Balance por Empréstimo
    balance_dummies = pd.get_dummies(balance[['sk_id_bureau', 'status']], columns=['status'])
    balance_agg = balance_dummies.groupby('sk_id_bureau').sum().reset_index()
    
    # Junta com Bureau e cria Ratios
    bureau = bureau.merge(balance_agg, on='sk_id_bureau', how='left')
    bureau['is_active'] = (bureau['credit_active'] == 'Active').astype(int)
    bureau['debt_ratio'] = bureau['amt_credit_sum_debt'] / bureau['amt_credit_sum']
    bureau['debt_ratio'] = bureau['debt_ratio'].replace([np.inf, -np.inf], np.nan)

    # Agrega por Cliente (SK_ID_CURR)
    bureau_agg = bureau.groupby('sk_id_curr').agg({
        'sk_id_bureau': 'count',
        'days_credit': ['min', 'mean'],
        'amt_credit_sum': ['sum', 'max'],
        'amt_credit_sum_debt': ['sum'],
        'amt_credit_max_overdue': ['max'],
        'is_active': ['sum'],
        'status_1': ['sum'], # Atrasos leves no balance
        'status_5': ['sum']  # Atrasos graves no balance
    })
    
    bureau_agg.columns = ['BUREAU_' + '_'.join(col).upper() for col in bureau_agg.columns]
    save_atomic_parquet(bureau_agg.reset_index(), "dim_bureau.parquet")

# ==============================================================================
# PREVIOUS APPLICATION
# ==============================================================================
def process_previous_application():
    print("Processando: Previous Application...")
    prev = pd.read_parquet(os.path.join(BRONZE_PATH, "previous_application.parquet"))
    
    # TRATATIVA EDA: Substituir 365243 por NaN 
    cols_dias = [col for col in prev.columns if 'days_' in col]
    for col in cols_dias:
        prev[col] = prev[col].replace(365243, np.nan)
        
    # Flags de Negócio
    prev['is_approved'] = (prev['name_contract_status'] == 'Approved').astype(int)
    prev['is_refused'] = (prev['name_contract_status'] == 'Refused').astype(int)

    # Agrega por Cliente
    prev_agg = prev.groupby('sk_id_curr').agg({
        'sk_id_prev': 'count',
        'amt_application': ['min', 'max', 'mean'],
        'amt_credit': ['sum'],
        'is_approved': ['sum', 'mean'],
        'is_refused': ['sum', 'mean'],
        'days_decision': ['max', 'mean']
    })
    
    prev_agg.columns = ['PREV_' + '_'.join(col).upper() for col in prev_agg.columns]
    save_atomic_parquet(prev_agg.reset_index(), "dim_previous_app.parquet")

# ==============================================================================
# INSTALLMENTS PAYMENTS
# ==============================================================================
def process_installments():
    print(" Processando: Installments Payments...")
    inst = pd.read_parquet(os.path.join(BRONZE_PATH, "installments_payments.parquet"))
    
    # TRATATIVA: Dias de atraso e Fração de Pagamento
    inst['days_past_due'] = (inst['days_entry_payment'] - inst['days_instalment']).clip(lower=0)
    inst['payment_fraction'] = inst['amt_payment'] / inst['amt_instalment']
    inst['payment_fraction'] = inst['payment_fraction'].replace([np.inf, -np.inf], np.nan)
    
    inst_agg = inst.groupby('sk_id_curr').agg({
        'sk_id_prev': 'nunique',
        'days_past_due': ['max', 'mean', 'sum'],
        'payment_fraction': ['mean', 'min'],
        'amt_payment': ['sum', 'mean']
    })
    
    inst_agg.columns = ['INSTAL_' + '_'.join(col).upper() for col in inst_agg.columns]
    save_atomic_parquet(inst_agg.reset_index(), "dim_installments.parquet")

# ==============================================================================
# CREDIT CARD BALANCE
# ==============================================================================
def process_credit_card():
    print("Processando: Credit Card Balance...")
    cc = pd.read_parquet(os.path.join(BRONZE_PATH, "credit_card_balance.parquet"))
    
    # TRATATIVA EDA: 20% nulos nas colunas de amount. (sem movimentação)
    amt_cols = [col for col in cc.columns if 'amt_' in col]
    cc[amt_cols] = cc[amt_cols].fillna(0)
    
    # TRATATIVA EDA: Capturando o risco de saques no caixa eletrônico (ATM)
    cc['has_atm_drawing'] = (cc['amt_drawings_atm_current'] > 0).astype(int)
    
    cc_agg = cc.groupby('sk_id_curr').agg({
        'sk_id_prev': 'nunique',
        'months_balance': ['min', 'count'],
        'amt_balance': ['max', 'mean'],
        'amt_credit_limit_actual': ['max'],
        'has_atm_drawing': ['sum', 'mean']
    })
    
    cc_agg.columns = ['CC_' + '_'.join(col).upper() for col in cc_agg.columns]
    save_atomic_parquet(cc_agg.reset_index(), "dim_credit_card.parquet")

# ==============================================================================
#  POS CASH BALANCE
# ==============================================================================
def process_pos_cash():
    print("Processando: POS Cash Balance...")
    pos = pd.read_parquet(os.path.join(BRONZE_PATH, "pos_cash_balance.parquet"))
    
    # TRATATIVA EDA: O status Active domina (~91.5%). Incluindo Completed também.
    pos['is_active'] = (pos['name_contract_status'] == 'Active').astype(int)
    pos['is_completed'] = (pos['name_contract_status'] == 'Completed').astype(int)
    
    pos_agg = pos.groupby('sk_id_curr').agg({
        'sk_id_prev': 'nunique',
        'months_balance': ['min', 'count'],
        'cnt_instalment_future': ['max', 'mean'],
        'is_active': ['sum', 'mean'],
        'is_completed': ['sum']
    })
    
    pos_agg.columns = ['POS_' + '_'.join(col).upper() for col in pos_agg.columns]
    save_atomic_parquet(pos_agg.reset_index(), "dim_pos_cash.parquet")

def run_pipeline():
    os.makedirs(SILVER_PATH, exist_ok=True)
    print("Iniciando Pipeline de Dimensões (Fase 2.b)")
    process_bureau()
    process_previous_application()
    process_installments()
    process_credit_card()
    process_pos_cash()
    print("Pipeline Finalizado com Sucesso!")

if __name__ == "__main__":
    run_pipeline()