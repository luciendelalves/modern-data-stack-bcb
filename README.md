# Modern Data Stack — Banco Central do Brasil

Pipeline de dados para extração, armazenamento e análise de indicadores
econômicos brasileiros usando dados públicos do Banco Central.

---

## Contexto

O Banco Central do Brasil disponibiliza uma API pública com indicadores
econômicos como câmbio, Selic e IPCA. O objetivo foi construir um pipeline
que consome essa API, armazena os dados em um banco analítico e permite
consultas SQL diretas sobre os indicadores.

---

## Stack

- Python — extração e carga
- DuckDB — banco de dados analítico (OLAP)
- pandas — manipulação dos dados
- API pública do BCB — fonte de dados

---

## Indicadores disponíveis

- Taxa de câmbio USD/BRL
- Taxa Selic (em desenvolvimento)
- IPCA (em desenvolvimento)

---

## Estrutura
```
modern-data-stack-bcb/
├── src/
│   ├── extract/
│   │   └── extrair_e_carregar.py
│   └── utils/
├── sql/
├── notebooks/
├── tests/
└── requirements.txt
```

---

## Como executar

**Pré-requisitos:** Python 3.8+
```bash
# 1. Clone o repositório
git clone https://github.com/luciendelalves/modern-data-stack-bcb.git
cd modern-data-stack-bcb

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o pipeline de extração
python src/extract/extrair_e_carregar.py

# 5. Consulte os dados
python src/consultar_dados.py
```

---

## Exemplos de análise

Estatísticas do dólar:
```sql
SELECT
    COUNT(*)                            AS total_registros,
    ROUND(MIN(cotacaoCompra), 4)        AS menor_cotacao,
    ROUND(MAX(cotacaoCompra), 4)        AS maior_cotacao,
    ROUND(AVG(cotacaoCompra), 4)        AS media_cotacao
FROM raw_cotacoes_usd;
```

Dias de maior variação:
```sql
SELECT
    DATE(dataHoraCotacao)                               AS data,
    ROUND(MAX(cotacaoCompra) - MIN(cotacaoCompra), 4)   AS variacao_dia
FROM raw_cotacoes_usd
GROUP BY DATE(dataHoraCotacao)
ORDER BY variacao_dia DESC
LIMIT 10;
```

---

## Próximos passos

- Adicionar indicadores Selic e IPCA
- Implementar dbt para transformações
- Testes de qualidade de dados
- Dashboard com Metabase ou Evidence
- CI/CD com GitHub Actions

---

## Autor

**Luciendel Alves**
Analista de Risco & PLD — iGaming
[LinkedIn](https://www.linkedin.com/in/luciendel-alves-008321107/) ·
[GitHub](https://github.com/luciendelalves)