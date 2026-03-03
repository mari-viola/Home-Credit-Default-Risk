# 📊 Home Credit Default Risk: End-to-End Data Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Architecture](https://img.shields.io/badge/Architecture-Medallion-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Contexto e Introdução

Este projeto foi desenvolvido sob a perspectiva de um **Engenheiro de Analytics**, responsável por arquitetar a fundação de dados que conecta a matéria-prima (dados brutos e dispersos) à inteligência de negócio.

No cenário atual de Big Data, o desafio não é apenas armazenar dados, mas torná-los acessíveis, confiáveis e prontos para o consumo. Este repositório simula um ambiente corporativo onde é necessário estruturar, transformar e analisar grandes volumes de dados financeiros para habilitar times de **Data Science** e **Produto** na criação de modelos preditivos e estratégias de mercado.

## 🎯 Objetivo do Projeto

Construir um **Pipeline Analítico Robusto** que processe as bases de dados relacionais complexas do desafio *"Home Credit Default Risk"*, gerando uma camada analítica consolidada e governada.

Os objetivos específicos são:

1.  **Engenharia de Dados & Qualidade:** Implementar um fluxo de ingestão e transformação resiliente (ETL/ELT), garantindo a limpeza, tipagem e integridade dos dados desde a origem até o consumo.
2.  **Preparação para Machine Learning (Feature Engineering):** Disponibilizar um dataset analítico final (*One Big Table* - Gold Layer) enriquecido com variáveis explicativas, pronto para alimentar modelos de Credit Scoring.
3.  **Analytics & Tomada de Decisão:** Construir visualizações interativas e KPIs que permitam a identificação rápida de padrões de inadimplência e a validação de hipóteses de negócio.

## 📍 Detalhes do Pipeline (Arquitetura Medallion)

O pipeline foi desenhado para processar dados relacionais complexos com cardinalidade 1:N. Abaixo, o detalhamento técnico de cada estágio:

### 1. Ingestão (Raw → Bronze)
* **Objetivo:** Padronização e Performance.
* **Processo:** Leitura dos arquivos CSV originais e conversão imediata para formato **Parquet** com compressão Snappy.
* **Destaque:** Implementação de escrita atômica (arquivos `.tmp`) para garantir integridade em caso de falha de gravação e redução drástica do espaço em disco.

### 2. Refinamento (Bronze → Silver)
* **Objetivo:** Limpeza e Normalização.
* **Processo:**
    * Tratamento de anomalias (ex: substituição de valores `365243` em dias de emprego por `NaN`).
    * Padronização de tipos de dados (casting).
    * **Agregação de Dimensões:** Tratamento de tabelas transacionais (como *Bureau* e *Installments*) reduzindo a cardinalidade para 1 linha por cliente (Group By SK_ID_CURR) através de médias, somas e contagens.

### 3. Modelagem Analítica (Silver → Gold)
* **Objetivo:** Enriquecimento e Consumo.
* **Processo:**
    * Joins finais entre a tabela de aplicação limpa e as dimensões agregadas.
    * **Feature Engineering:** Criação de variáveis de negócio, como `credit_income_ratio` (comprometimento de renda) e `ext_source_mean` (score consolidado).
    * Geração de uma **One Big Table (OBT)** pronta para alimentar modelos de ML ou Dashboards.

### 4. Visualização (Streamlit)
* **Objetivo:** Suporte à Decisão.
* **Processo:** Dashboard interativo que consome a camada Gold (com amostragem otimizada para web) para validar hipóteses de risco, comparando métricas do filtro selecionado *versus* a média global da empresa.

---

## 📂 Estrutura do Projeto

```text
├── data/                 # Data Lake local (ignorado no git)
├── docs/                 # Documentação técnica detalhada
├── notebooks/            # Análises Exploratórias (EDA) e Validação
├── src/                  # Código Fonte do Pipeline
│   ├── 01_ingestion.py           # Ingestão (Raw -> Bronze)
│   ├── 02_transform_application.py # Limpeza Tabela Principal
│   ├── 02b_transform_dimensions.py # Agregação Tabelas 1:N
│   ├── 03_analytical_layer.py    # Feature Eng. & Gold OBT
│   ├── pipeline.py               # Orquestrador Central
│   └── dashboard.py              # Aplicação Streamlit
├── tests/                # Testes Unitários e de Integração
├── .env.example          # Template de variáveis de ambiente
├── pyproject.toml        # Configuração de ferramentas
├── requirements.txt      # Dependências do projeto
└── README.md
```

## 🛠️ Pré-requisitos
Python 3.8+

Dados de entrada:[ Home Credit Default Risk (Kaggle)](https://www.kaggle.com/competitions/home-credit-default-risk/overview)

Baixe os arquivos e posicione-os na pasta data/raw/ (conforme documentado em docs/).

## ⚙️ Configuração e Instalação
Clone o repositório e crie o ambiente virtual:

```Bash
git clone [https://github.com/mari-viola/Home-Credit-Default-Risk.git](https://github.com/mari-viola/Home-Credit-Default-Risk.git)
cd Home-Credit-Default-Risk

python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```
Instale as dependências:

```Bash
pip install -r requirements.txt
```

Configure as variáveis de ambiente:

Crie um arquivo .env na raiz do projeto baseado no exemplo:

```Bash
# Windows
copy .env.example .env
# Linux/macOS
cp .env.example .env

```
Edite o arquivo .env para apontar para seus caminhos locais de dados.

## ▶️ Execução do Pipeline
Você pode rodar o pipeline completo ou etapas individuais via módulo:

Pipeline Completo (Orquestrador):

```Bash
python -m src.pipeline
```
Etapas Individuais (Modular):

```Bash
# 1. Ingestão (Raw -> Bronze)
python -m src.01_ingestion

# 2. Transformação (Bronze -> Silver)
python -m src.02_transform_application
python -m src.02b_transform_dimensions

# 3. Camada Analítica (Silver -> Gold)
python -m src.03_analytical_layer
```

## 📊 Visualização (Dashboard)
O projeto inclui um dashboard interativo desenvolvido em Streamlit para análise de inadimplência, perfil de clientes e validação de hipóteses.

Acesse Online:
👉 [Clique aqui para ver o Dashboard ao vivo](https://home-credit-default-risk-laugfy9bnnbkjucpa8zhdc.streamlit.app/)

Executar Localmente:

```Bash
streamlit run src/dashboard.py
```
## ✅ Testes
Para garantir a integridade do código e dos dados, execute a suíte de testes automatizados:

```Bash
pytest tests/ -v
```

## 📚 Documentação Complementar
Arquitetura de Dados: [Ver Diagrama e Modelo](https://github.com/mari-viola/Home-Credit-Default-Risk/blob/main/docs/ARCHITECTURE.md)

Relatório de Insights de Negócio: [Ver Análise Fase 4](https://github.com/mari-viola/Home-Credit-Default-Risk/blob/main/docs/RELATORIO_INSIGHTS.md)

Guia Rápido: [Index]([https://www.google.com/search?q=docs/INDEX.md](https://github.com/mari-viola/Home-Credit-Default-Risk/blob/main/docs/INDEX.md))

Apresentação do Projeto: [Ver Slides Explicativos (Google Slides)](https://docs.google.com/presentation/d/1kQCmytSamsoO-VmoA7ehcAnfgfrLcEU6WvJZZAb0ZqU/edit?slide=id.p1#slide=id.p1)


Autor: Mariana Viola
Projeto desenvolvido para fins de portfólio e estudo de arquiteturas de Big Data.
