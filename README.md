# 🏦 Modern Data Stack - Banco Central do Brasil

Pipeline de dados moderno para análise de indicadores econômicos brasileiros utilizando dados públicos do Banco Central.

## 📊 Sobre o Projeto

Este projeto demonstra a construção de um **Modern Data Stack** completo utilizando ferramentas open-source para extração, transformação e análise de dados econômicos do Brasil.

### Dados Utilizados
- **Fonte**: API pública do Banco Central do Brasil (BCB)
- **Indicadores**: 
  - Taxa de câmbio (USD/BRL)
  - Taxa Selic (em desenvolvimento)
  - IPCA (em desenvolvimento)

## 🛠️ Stack Tecnológico

- **Python 3.x**: Linguagem principal
- **DuckDB**: Banco de dados analítico (OLAP)
- **dbt** *(em breve)*: Transformação de dados (ELT)
- **Pandas**: Manipulação de dados
- **APIs REST**: Ingestão de dados

## 📁 Estrutura do Projeto

```
modern-data-stack-bcb/
├── data/              # Bancos de dados (não versionado)
├── src/               # Código fonte
│   ├── extract/      # Scripts de extração de APIs
│   └── utils/        # Funções utilitárias
├── notebooks/        # Análises exploratórias
├── sql/              # Queries SQL
├── docs/             # Documentação
└── tests/            # Testes automatizados
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- pip

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/modern-data-stack-bcb.git
cd modern-data-stack-bcb
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executar Pipeline de Extração

```bash
python src/extract/extrair_e_carregar.py
```

### Consultar Dados

```bash
python src/consultar_dados.py
```

## 📈 Exemplos de Análises

### Estatísticas do Dólar
```sql
SELECT 
    COUNT(*) as total_registros,
    ROUND(MIN(cotacaoCompra), 4) as menor_cotacao,
    ROUND(MAX(cotacaoCompra), 4) as maior_cotacao,
    ROUND(AVG(cotacaoCompra), 4) as media_cotacao
FROM raw_cotacoes_usd;
```

### Variação Diária
```sql
SELECT 
    DATE(dataHoraCotacao) as data,
    ROUND(MAX(cotacaoCompra) - MIN(cotacaoCompra), 4) as variacao_dia
FROM raw_cotacoes_usd
GROUP BY DATE(dataHoraCotacao)
ORDER BY variacao_dia DESC
LIMIT 10;
```

## 🎯 Roadmap

- [x] Extração de dados de câmbio (USD)
- [x] Armazenamento em DuckDB
- [x] Queries SQL básicas
- [ ] Adicionar mais indicadores (Selic, IPCA)
- [ ] Implementar dbt para transformações
- [ ] Criar testes de qualidade de dados
- [ ] Dashboard com Evidence/Metabase
- [ ] CI/CD com GitHub Actions
- [ ] Documentação automática com dbt docs

## 📚 Aprendizados

Este projeto demonstra:
- Consumo de APIs REST públicas
- Modelagem de dados para análise (OLAP)
- Uso de DuckDB para analytics
- Boas práticas de engenharia de dados
- Estruturação de projetos Python

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests.

## 📝 Licença

Este projeto está sob a licença MIT.

## 📧 Contato

- **Nome**: [Seu Nome]
- **LinkedIn**: [Seu LinkedIn]
- **Email**: [Seu Email]

---

⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!
