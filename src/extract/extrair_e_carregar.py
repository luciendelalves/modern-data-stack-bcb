"""
Pipeline de Extração e Carga (EL do ELT)
Busca dados do Banco Central e salva no DuckDB
"""

import requests
import duckdb
import pandas as pd
from datetime import datetime, timedelta

print("="*80)
print("🏦 PIPELINE DE DADOS - BANCO CENTRAL → DUCKDB")
print("="*80 + "\n")

# ==============================================================================
# ETAPA 1: EXTRAÇÃO (Extract)
# ==============================================================================

print("📥 ETAPA 1: EXTRAINDO DADOS DA API DO BANCO CENTRAL\n")

# Configurar período (últimos 30 dias para ter mais dados)
data_fim = datetime.now()
data_inicio = data_fim - timedelta(days=30)

data_inicio_str = data_inicio.strftime("%m-%d-%Y")
data_fim_str = data_fim.strftime("%m-%d-%Y")

print(f"📅 Período: {data_inicio_str} até {data_fim_str}")

# Montar URL da API
base_url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata"
url = f"{base_url}/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
url += f"?@moeda='USD'&@dataInicial='{data_inicio_str}'&@dataFinalCotacao='{data_fim_str}'"
url += "&$format=json"

try:
    # Fazer requisição
    print("⏳ Fazendo requisição...")
    response = requests.get(url, timeout=30)
    
    if response.status_code == 200:
        dados = response.json()
        cotacoes = dados.get('value', [])
        
        print(f"✅ Sucesso! {len(cotacoes)} registros extraídos\n")
        
        # Converter para DataFrame do Pandas (tipo uma tabela Excel)
        df = pd.DataFrame(cotacoes)
        
        print("📊 Primeiras 3 linhas dos dados:")
        print(df.head(3))
        print()
        
    else:
        print(f"❌ Erro: API retornou código {response.status_code}")
        exit(1)
        
except Exception as e:
    print(f"❌ Erro na extração: {e}")
    exit(1)

# ==============================================================================
# ETAPA 2: CARGA (Load)
# ==============================================================================

print("\n" + "="*80)
print("💾 ETAPA 2: CARREGANDO DADOS NO DUCKDB\n")

try:
    # Conectar ao DuckDB (se o arquivo não existe, ele cria automaticamente)
    # É como abrir um arquivo Excel - se não existe, cria um novo
    conn = duckdb.connect('bcb_data.duckdb')
    
    print("📁 Banco de dados: bcb_data.duckdb")
    
    # Criar tabela (se já existir, substitui - por enquanto)
    # Estamos salvando os dados "crus" vindos da API
    print("📝 Criando tabela 'raw_cotacoes_usd'...")
    
    conn.execute("""
        CREATE OR REPLACE TABLE raw_cotacoes_usd AS 
        SELECT * FROM df
    """)
    
    # Contar quantas linhas foram inseridas
    resultado = conn.execute("SELECT COUNT(*) as total FROM raw_cotacoes_usd").fetchone()
    total_linhas = resultado[0]
    
    print(f"✅ Tabela criada! {total_linhas} linhas inseridas\n")
    
except Exception as e:
    print(f"❌ Erro ao carregar no DuckDB: {e}")
    exit(1)

# ==============================================================================
# ETAPA 3: VERIFICAÇÃO
# ==============================================================================

print("="*80)
print("🔍 ETAPA 3: VERIFICANDO OS DADOS SALVOS\n")

# Consulta 1: Ver estrutura da tabela
print("1️⃣ Estrutura da tabela:")
print()
estrutura = conn.execute("DESCRIBE raw_cotacoes_usd").fetchdf()
print(estrutura)
print()

# Consulta 2: Primeiros registros
print("\n2️⃣ Primeiros 5 registros salvos:")
print()
primeiros = conn.execute("""
    SELECT 
        dataHoraCotacao,
        cotacaoCompra,
        cotacaoVenda
    FROM raw_cotacoes_usd
    ORDER BY dataHoraCotacao DESC
    LIMIT 5
""").fetchdf()
print(primeiros)
print()

# Consulta 3: Estatísticas básicas
print("\n3️⃣ Estatísticas das cotações:")
print()
stats = conn.execute("""
    SELECT 
        COUNT(*) as total_registros,
        MIN(cotacaoCompra) as menor_cotacao,
        MAX(cotacaoCompra) as maior_cotacao,
        AVG(cotacaoCompra) as media_cotacao,
        MIN(dataHoraCotacao) as data_mais_antiga,
        MAX(dataHoraCotacao) as data_mais_recente
    FROM raw_cotacoes_usd
""").fetchdf()
print(stats)
print()

# Fechar conexão
conn.close()

print("="*80)
print("✅ PIPELINE EXECUTADO COM SUCESSO!")
print("="*80)
print()
print("📂 Arquivo criado: bcb_data.duckdb")
print("📊 Tabela criada: raw_cotacoes_usd")
print()
print("💡 PRÓXIMOS PASSOS:")
print("   1. Você pode abrir o arquivo bcb_data.duckdb com qualquer ferramenta SQL")
print("   2. Vamos criar transformações dbt em cima desses dados")
print("   3. Vamos adicionar mais fontes de dados (Selic, inflação, etc)")
print()
