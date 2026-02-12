# Relatório de Insights – Risco de Crédito (Home Credit)

Relatório com achados relevantes sobre inadimplência, a partir da camada analítica (Gold/OBT) e do notebook `notebooks/03_analytical_metrics.ipynb`.

---

## Contexto

- **Base:** Home Credit Default Risk (aplicações de crédito).
- **Target:** Inadimplência (0 = pago, 1 = default).
- **Camada analítica:** One Big Table (OBT) em `data/gold/analytics_credit_risk_train.parquet` (~307k linhas, 177+ features).

---

## 1. Taxa global de inadimplência

- **Taxa de default global:** ~8,07%.
- Base desbalanceada (maioria bons pagadores); relevante para métricas e amostragem em modelagem.

---

## 2. Taxa de default por tipo de contrato

- Empréstimos em **dinheiro vivo** tendem a apresentar **maior taxa de default** que modalidades como crédito rotativo.
- **Insight:** Tipo de contrato é um sinal forte de risco; útil para segmentação e políticas de limite.

---

## 3. Taxa de default por faixa de renda (quintis)

- Renda segmentada em 5 faixas (quintis).
- **Tendência:** Maior renda associada a **menor taxa de inadimplência**.
- **Insight:** Renda é um preditor importante; faixas de renda mais baixa devem ter critérios e limites diferenciados.

---

## 4. Idade e risco

- **Faixas etárias:** 20–30, 31–40, 41–50, 51–60, 60+.
- **Achado:** Idade maior tende a estar associada a **menor taxa de default** (ex.: idade média de bons pagadores > idade média de maus pagadores).
- **Insight:** Idade pode ser usada como variável de segmentação e em modelos de scoring.

---

## 5. Feature de risco externo (`ext_source_mean`)

- `ext_source_mean` é uma feature derivada (média dos scores externos).
- **Validação:** Quando segmentada em quartis, as faixas com **score externo mais alto** apresentam **menor taxa de default**.
- **Insight:** A consolidação dos scores externos (feature engineering) captura bem o sinal de risco e deve ser mantida na modelagem.

---

## Recomendações resumidas

1. **Modelagem:** Usar tipo de contrato, faixa de renda, idade e `ext_source_mean` como candidatos fortes a features.
2. **Produto/Política:** Considerar limites e critérios mais conservadores para contratos em dinheiro vivo e faixas de menor renda.
3. **Monitoramento:** Acompanhar taxa de default por faixa de renda, tipo de contrato e faixa etária para detectar mudanças no perfil de risco.

---

*Relatório alinhado à Tarefa 4 do desafio técnico (Visualização e Comunicação). Métricas detalhadas e gráficos estão em `notebooks/03_analytical_metrics.ipynb` e no dashboard (`src/dashboard.py`).*
