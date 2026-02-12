# Pipeline de Dados - Credit Risk (Avaliação Itaú)

Pipeline de ingestão e transformação de dados em camadas (Raw → Bronze → Silver → Gold) para análise de crédito.

## Estrutura do projeto

```
├── data/                 # Dados (raw, bronze, silver, gold)
├── docs/                 # Documentação técnica completa
├── notebooks/            # EDA e análises
├── src/                  # Código do pipeline
│   ├── 01_ingestion.py           # Raw → Bronze
│   ├── 02_transform_application.py
│   ├── 02b_transform_dimensions.py
│   ├── 03_analytical_layer.py    # Silver → Gold
│   ├── pipeline.py               # Orquestração
│   └── dashboard.py              # Dashboard Streamlit (Tarefa 4)
├── tests/                # Testes automatizados
├── .env.example          # Exemplo de variáveis de ambiente
├── pyproject.toml        # Metadados e dependências
├── requirements.txt      # Dependências pip
└── README.md
```

## Pré-requisitos

- Python 3.8+
- Dados de entrada em `data/raw/` (CSV conforme documentado em `docs/`)

## Configuração

1. Crie um ambiente virtual e instale as dependências:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # Linux/macOS
   pip install -r requirements.txt
   ```

2. Configure as variáveis de ambiente. Copie o exemplo e edite:

   ```bash
   copy .env.example .env   # Windows
   # cp .env.example .env   # Linux/macOS
   ```

   Edite `.env` e defina pelo menos:

   - `RAW_DATA_PATH` – pasta com os CSV de entrada (ex.: `data/raw`)
   - `BRONZE_DATA_PATH` – pasta de saída Bronze (ex.: `data/bronze`)
   - `SILVER_DATA_PATH` – (opcional) padrão: `data/silver`
   - `GOLD_DATA_PATH` – (opcional) padrão: `data/gold`

## Execução

**Pipeline completo (da raiz do projeto):**

```bash
python -m src.pipeline
```

**Etapas individuais:**

```bash
python -m src.01_ingestion
python -m src.02_transform_application
python -m src.02b_transform_dimensions
python -m src.03_analytical_layer
```

**Dashboard (insights sobre inadimplência):**

```bash
pip install streamlit   # já está em requirements.txt
streamlit run src/dashboard.py
```
- Streamlit Link: https://home-credit-default-risk-laugfy9bnnbkjucpa8zhdc.streamlit.app/#dashboard-de-risco-de-credito-home-credit


**Testes:**

```bash
pip install pytest
pytest tests/ -v
```

## Documentação

- **Índice e quick start:** [docs/INDEX.md](docs/INDEX.md)
- **Modelo de dados / diagrama:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Relatório de insights (Fase 4):** [docs/RELATORIO_INSIGHTS.md](docs/RELATORIO_INSIGHTS.md)

## Licença

Uso interno / avaliação.
