# 📊 Home Credit Default Risk: End-to-End Data Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Architecture](https://img.shields.io/badge/Architecture-Medallion-green)

Este projeto implementa um pipeline de Engenharia de Dados completo para análise de risco de crédito, transformando dados brutos em insights de negócio. A arquitetura segue o padrão **Medallion (Bronze, Silver, Gold)**, garantindo governança, rastreabilidade e performance.

O resultado final é uma camada analítica robusta (OBT) e um Dashboard interativo para identificação de padrões de inadimplência.

---

## 🚀 Funcionalidades e Arquitetura

O pipeline processa dados relacionais complexos (1:N) através das seguintes etapas:

1.  **Ingestão (Raw → Bronze):** Conversão de CSV para Parquet com tipagem estrita e compressão (Snappy).
2.  **Refinamento (Bronze → Silver):** Limpeza de dados, tratamento de valores nulos, remoção de anomalias e agregações de tabelas transacionais (Bureau, Installments).
3.  **Modelagem Analítica (Silver → Gold):** Consolidação em uma *One Big Table* (OBT), criação de novas *features* (Feature Engineering) e cálculo de KPIs de risco.
4.  **Visualização:** Dashboard interativo para exploração de dados e suporte à decisão.

## 📂 Estrutura do Projeto

```text
├── data/                 # Data Lake local (ignorado no git)
├── docs/                 # Documentação técnica detalhada
├── notebooks/            # Análises Exploratórias (EDA) e Validação
├── src/                  # Código Fonte do Pipeline
│   ├── 01_ingestion.py           # Ingestão e Padronização
│   ├── 02_transform_application.py
│   ├── 02b_transform_dimensions.py
│   ├── 03_analytical_layer.py    # Construção da Tabela Ouro
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

Dados de entrada (Dataset Home Credit) posicionados em data/raw/

## ⚙️ Configuração e Instalação
Clone o repositório e crie o ambiente virtual:

```Bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_REPO.git](https://github.com/SEU_USUARIO/NOME_DO_REPO.git)
cd NOME_DO_REPO

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
Arquitetura de Dados: [Ver Diagrama e Modelo](https://www.google.com/search?q=docs/ARCHITECTURE.md)

Relatório de Insights de Negócio: [Ver Análise Fase 4](https://www.google.com/search?q=docs/RELATORIO_INSIGHTS.md)

Guia Rápido: [Index](https://www.google.com/search?q=docs/INDEX.md)

Autor: Mariana Viola
Projeto desenvolvido para fins de portfólio e estudo de arquiteturas de Big Data.
