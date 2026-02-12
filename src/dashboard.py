import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np

# Configuração da Página
st.set_page_config(page_title="Credit Risk Dashboard", layout="wide")

# Cache para não recarregar dados pesados
@st.cache_data
def load_data():
    # Ajuste o caminho conforme necessário
    path = os.path.join("data", "gold", "analytics_credit_risk_train.parquet")
    if not os.path.exists(path):
        st.error("Arquivo OBT não encontrado. Rode o pipeline primeiro!")
        return None
    
    df = pd.read_parquet(path)
    # Amostragem para performance (opcional, remova se quiser ver tudo)
    return df.sample(50000) if len(df) > 50000 else df

df = load_data()

if df is not None:
    # --- SIDEBAR (FILTROS) ---
    st.sidebar.header("Filtros")
    tipos_contrato = st.sidebar.multiselect(
        "Tipo de Contrato:", 
        options=df['name_contract_type'].unique(),
        default=df['name_contract_type'].unique()
    )
    
    df_filtered = df[df['name_contract_type'].isin(tipos_contrato)]

    # --- TÍTULO E KPIS ---
    st.title(" Dashboard de Risco de Crédito - Home Credit")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    
    total_clientes = len(df_filtered)
    taxa_default = df_filtered['target'].mean() * 100
    renda_media = df_filtered['amt_income_total'].mean()
    idade_media = df_filtered['years_birth'].mean()

    col1.metric("Total de Clientes", f"{total_clientes:,.0f}")
    col2.metric("Taxa de Default Global", f"{taxa_default:.2f}%", "-Risco")
    col3.metric("Renda Média", f"R$ {renda_media:,.2f}")
    col4.metric("Idade Média", f"{idade_media:.0f} anos")

    st.markdown("---")

    # --- LINHA 1: GRÁFICOS PRINCIPAIS ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("1. Risco por Faixa de Renda (Quintis)")
        # Cria faixas de renda dinamicamente
        df_filtered['faixa_renda'] = pd.qcut(df_filtered['amt_income_total'], q=5, labels=['E', 'D', 'C', 'B', 'A'])
        risk_by_income = df_filtered.groupby('faixa_renda', observed=True)['target'].mean().reset_index()
        
        fig_income = px.bar(
            risk_by_income, x='faixa_renda', y='target',
            title="Inadimplência cai conforme Renda aumenta?",
            labels={'target': 'Taxa de Default', 'faixa_renda': 'Classe de Renda'},
            color='target', color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_income, use_container_width=True)

    with c2:
        st.subheader("2. Distribuição de Idade: Bons vs Maus Pagadores")
        fig_age = px.histogram(
            df_filtered, x="years_birth", color="target",
            barmode="overlay", nbins=30,
            title="Os jovens são mais arriscados?",
            labels={'years_birth': 'Idade', 'target': 'Default (0=Não, 1=Sim)'},
            opacity=0.75
        )
        st.plotly_chart(fig_age, use_container_width=True)

    # --- LINHA 2: INSIGHTS SECUNDÁRIOS ---
    c3, c4 = st.columns(2)

    with c3:
        st.subheader("3. Risco por Tipo de Ocupação")
        risk_by_job = df_filtered.groupby('occupation_type')['target'].mean().sort_values(ascending=False).head(10).reset_index()
        fig_job = px.bar(
            risk_by_job, y='occupation_type', x='target', orientation='h',
            title="Top 10 Profissões com Maior Risco",
            color='target', color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_job, use_container_width=True)

    with c4:
        st.subheader("4. Correlação: Score Externo vs Default")
        # Binagem do score externo
        df_filtered['score_bin'] = pd.cut(df_filtered['ext_source_mean'], bins=10)
        risk_by_score = df_filtered.groupby('score_bin', observed=True)['target'].mean().reset_index()
        # Convert interval to string for plotting
        risk_by_score['score_bin'] = risk_by_score['score_bin'].astype(str)
        
        fig_score = px.line(
            risk_by_score, x='score_bin', y='target', markers=True,
            title="O Score Externo prevê o calote?",
            labels={'score_bin': 'Faixas de Score Externo (Baixo -> Alto)'}
        )
        st.plotly_chart(fig_score, use_container_width=True)