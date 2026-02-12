# Índice da Documentação

Documentação técnica do pipeline, organizada por fase (desafio técnico Eng. Analytics).

---

## Modelo de dados e arquitetura

- **[ARCHITECTURE.md](ARCHITECTURE.md)** – Diagrama do pipeline, comparação Raw/Bronze/Silver/Gold, validações e fluxo recomendado.

---

## Por fase

### Fase 1 – Ingestão e modelagem

- **[01_ingestion.md](01_ingestion.md)** – Processo de ingestão (Raw → Bronze), escrita atômica, Parquet, schema e execução.
- **[01b_modelagem_dados.md](01b_modelagem_dados.md)** – Justificativa das camadas, decisões de schema, tratamento de missing/outliers e qualidade.

### Fase 2 – Transformação e enriquecimento

- **[02_transform_application.md](02_transform_application.md)** – EDA, transformação da tabela fato (application), feature engineering e schema Silver.
- **[02b_eda_dimensions.md](02b_eda_dimensions.md)** – EDA e transformação das tabelas dimensionais (bureau, installments, etc.).

### Fase 3 – Camada analítica

- **[03_analytical_layer.md](03_analytical_layer.md)** – Construção da OBT (Gold), Star Schema vs. OBT e consumo para ML/BI.

### Fase 4 – Visualização e comunicação

- **[RELATORIO_INSIGHTS.md](RELATORIO_INSIGHTS.md)** – Relatório com achados sobre inadimplência (taxa global, tipo de contrato, faixa de renda, idade, score externo). Dashboard: `src/dashboard.py` (Streamlit).

---

## Quick start

```bash
# 1. Configurar .env (RAW_DATA_PATH, BRONZE_DATA_PATH; ver .env.example)
# 2. Pipeline completo
python -m src.pipeline

# Ou por etapa:
python -m src.01_ingestion
python -m src.02_transform_application
python -m src.02b_transform_dimensions
python -m src.03_analytical_layer

# Dashboard
streamlit run src/dashboard.py
```

---

**Estrutura da documentação:** `docs/` contém apenas os arquivos listados acima (modelo de dados + uma doc por fase).
