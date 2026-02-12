import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E CARGA DE DADOS
# ==============================================================================
st.set_page_config(
    page_title="Relatório de Risco de Crédito | Home Credit",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache para performance
@st.cache_data
def load_data():
    path = os.path.join("data", "gold", "analytics_credit_risk_train.parquet")
    
    if not os.path.exists(path):
        return None
    
    try:
        df = pd.read_parquet(path)
        # Amostragem de segurança para performance na web (50k linhas)
        # Se for rodar local com máquina potente, pode aumentar ou remover.
        return df.sample(50000, random_state=42) if len(df) > 50000 else df
    except Exception as e:
        st.error(f"Erro na leitura: {e}")
        return None

df = load_data()

if df is None:
    st.error("⚠️ Arquivo de dados não encontrado. Verifique se o pipeline (Fase 3) rodou com sucesso.")
    st.stop()

# ==============================================================================
# 2. CÁLCULO DE REFERÊNCIA GLOBAL (BENCHMARK)
# ==============================================================================
# Calculamos os indicadores globais ANTES de qualquer filtro para comparação
taxa_inadimplencia_global = df['target'].mean() * 100
renda_media_global = df['amt_income_total'].mean()

# ==============================================================================
# 3. BARRA LATERAL (FILTROS)
# ==============================================================================
st.sidebar.header("🔍 Filtros de Segmentação")
st.sidebar.markdown("*Selecione para filtrar. Deixe vazio para ver tudo.*")

# Função auxiliar para filtro inteligente (Vazio = Todos)
def smart_filter(df, column, selected_options):
    if not selected_options:
        return df
    return df[df[column].isin(selected_options)]

# Inputs do Usuário
sel_contrato = st.sidebar.multiselect("Tipo de Contrato:", df['name_contract_type'].unique())
sel_genero = st.sidebar.multiselect("Gênero:", df['code_gender'].unique())
sel_educacao = st.sidebar.multiselect("Nível de Educação:", df['name_education_type'].unique())

# Aplicação dos Filtros
df_filtered = df.copy()
df_filtered = smart_filter(df_filtered, 'name_contract_type', sel_contrato)
df_filtered = smart_filter(df_filtered, 'code_gender', sel_genero)
df_filtered = smart_filter(df_filtered, 'name_education_type', sel_educacao)

# Se o filtro zerar os dados, avisa o usuário
if df_filtered.empty:
    st.warning("⚠️ Nenhum dado encontrado para essa combinação de filtros.")
    st.stop()

# ==============================================================================
# 4. DASHBOARD - CABEÇALHO E KPIS
# ==============================================================================
st.title("📊 Relatório de Insights: Risco de Crédito")
st.markdown("Análise baseada na camada **Gold (OBT)** focada em identificar drivers de inadimplência.")
st.markdown("---")

# Métricas Principais
col1, col2, col3, col4 = st.columns(4)

curr_inadimplencia = df_filtered['target'].mean() * 100
curr_renda = df_filtered['amt_income_total'].mean()
curr_idade = df_filtered['years_birth'].mean()
total_clientes = len(df_filtered)

# Delta: Diferença entre o filtro atual e a média global da empresa
delta_inad = curr_inadimplencia - taxa_inadimplencia_global

with col1:
    st.metric("Total de Clientes (Filtro)", f"{total_clientes:,.0f}".replace(",", "."))

with col2:
    st.metric(
        "Taxa de Inadimplência", 
        f"{curr_inadimplencia:.2f}%", 
        f"{delta_inad:+.2f} p.p vs Global",
        delta_color="inverse" # Vermelho se subir (risco maior), Verde se cair
    )

with col3:
    st.metric(
        "Renda Média", 
        f"R$ {curr_renda:,.2f}",
        f"{((curr_renda - renda_media_global)/renda_media_global)*100:+.1f}% vs Global"
    )

with col4:
    st.metric("Idade Média", f"{curr_idade:.0f} anos")

st.markdown("---")

# ==============================================================================
# 5. VISUALIZAÇÕES DOS INSIGHTS (DO RELATÓRIO)
# ==============================================================================

# --- LINHA 1: RENDA E CONTRATO ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("1. Inadimplência por Faixa de Renda")
    st.caption("Insight: Renda maior está associada a menor risco? (Divisão em Quintis)")
    
    try:
        # Criação dos Quintis (E=Pobres, A=Ricos)
        df_filtered['faixa_renda'] = pd.qcut(
            df_filtered['amt_income_total'], 
            q=5, 
            labels=['E (Menor Renda)', 'D', 'C', 'B', 'A (Maior Renda)'],
            duplicates='drop'
        )
        
        # Agrupamento
        risco_renda = df_filtered.groupby('faixa_renda', observed=True)['target'].mean().reset_index()
        risco_renda['target'] = risco_renda['target'] * 100 # Para %
        
        fig_renda = px.bar(
            risco_renda, x='faixa_renda', y='target',
            labels={'target': 'Taxa de Inadimplência (%)', 'faixa_renda': 'Classe Social'},
            color='target', color_continuous_scale='Reds',
            text_auto='.2f'
        )
        fig_renda.update_layout(yaxis_title="Inadimplência (%)")
        st.plotly_chart(fig_renda, use_container_width=True)
    except:
        st.info("Dados insuficientes no filtro para calcular quintis de renda.")

with c2:
    st.subheader("2. Risco por Tipo de Contrato")
    st.caption("Insight: 'Cash Loans' (Dinheiro Vivo) são mais arriscados?")
    
    risco_contrato = df_filtered.groupby('name_contract_type', observed=True)['target'].mean().reset_index()
    risco_contrato['target'] = risco_contrato['target'] * 100
    
    # Tradução Visual
    risco_contrato['name_contract_type'] = risco_contrato['name_contract_type'].replace({
        'Cash loans': 'Empréstimo em Dinheiro',
        'Revolving loans': 'Crédito Rotativo'
    })
    
    fig_contrato = px.bar(
        risco_contrato, x='name_contract_type', y='target',
        labels={'target': 'Taxa de Inadimplência (%)', 'name_contract_type': 'Modalidade'},
        color='target', color_continuous_scale='Reds',
        text_auto='.2f'
    )
    fig_contrato.update_layout(yaxis_title="Inadimplência (%)")
    st.plotly_chart(fig_contrato, use_container_width=True)

# --- LINHA 2: IDADE E SCORE EXTERNO ---
c3, c4 = st.columns(2)

with c3:
    st.subheader("3. Risco por Faixa Etária")
    st.caption("Insight: Clientes mais velhos pagam melhor? (Bins: 20-30, 30-40...)")
    
    # Criação de Bins de Idade conforme o relatório
    bins = [20, 30, 40, 50, 60, 100]
    labels = ['20-30 anos', '31-40 anos', '41-50 anos', '51-60 anos', '60+ anos']
    df_filtered['faixa_etaria'] = pd.cut(df_filtered['years_birth'], bins=bins, labels=labels)
    
    risco_idade = df_filtered.groupby('faixa_etaria', observed=True)['target'].mean().reset_index()
    risco_idade['target'] = risco_idade['target'] * 100
    
    fig_idade = px.line(
        risco_idade, x='faixa_etaria', y='target', markers=True,
        labels={'target': 'Taxa de Inadimplência (%)', 'faixa_etaria': 'Idade'},
        color_discrete_sequence=['#FF4B4B'] # Vermelho Streamlit
    )
    fig_idade.update_layout(yaxis_title="Inadimplência (%)", yaxis_range=[0, max(risco_idade['target'])*1.2])
    st.plotly_chart(fig_idade, use_container_width=True)

with c4:
    st.subheader("4. Validação: Score Externo")
    st.caption("Insight: A feature 'ext_source_mean' realmente prevê o risco?")
    
    try:
        # Quartis do Score Externo
        df_filtered['score_quartil'] = pd.qcut(
            df_filtered['ext_source_mean'], 
            q=4, 
            labels=['Q1 (Score Baixo/Ruim)', 'Q2', 'Q3', 'Q4 (Score Alto/Bom)'],
            duplicates='drop'
        )
        
        risco_score = df_filtered.groupby('score_quartil', observed=True)['target'].mean().reset_index()
        risco_score['target'] = risco_score['target'] * 100
        
        fig_score = px.bar(
            risco_score, x='score_quartil', y='target',
            labels={'target': 'Inadimplência Real (%)', 'score_quartil': 'Quartil do Score'},
            color='target', color_continuous_scale='Greens_r', # Invertido: Verde é bom (baixo risco)
            text_auto='.2f'
        )
        fig_score.update_layout(yaxis_title="Inadimplência (%)")
        st.plotly_chart(fig_score, use_container_width=True)
    except:
        st.info("Score externo indisponível para este filtro.")

# --- RODAPÉ: DADOS BRUTOS ---
with st.expander("📋 Ver Amostra dos Dados (Tabela Detalhada)"):
    st.dataframe(
        df_filtered[['sk_id_curr', 'target', 'amt_income_total', 'name_contract_type', 'name_education_type', 'ext_source_mean']]
        .sort_values(by='amt_income_total', ascending=False)
        .head(100)
    )