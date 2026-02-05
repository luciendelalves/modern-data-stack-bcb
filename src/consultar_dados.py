"""
Script para consultar dados do DuckDB
Você pode rodar queries SQL e ver os resultados
"""

import duckdb
import sys

# Conectar ao banco
conn = duckdb.connect('bcb_data.duckdb', read_only=True)

print("="*80)
print("🦆 DUCKDB - CONSOLE DE CONSULTAS")
print("="*80)
print()
print("📂 Conectado a: bcb_data.duckdb")
print()

# ==============================================================================
# CONSULTAS PRÉ-DEFINIDAS
# ==============================================================================

print("📊 CONSULTAS DISPONÍVEIS:\n")

queries = {
    "1": {
        "nome": "Ver todas as tabelas do banco",
        "sql": "SHOW TABLES"
    },
    "2": {
        "nome": "Ver estrutura da tabela raw_cotacoes_usd",
        "sql": "DESCRIBE raw_cotacoes_usd"
    },
    "3": {
        "nome": "Primeiros 10 registros",
        "sql": """
            SELECT 
                dataHoraCotacao,
                cotacaoCompra,
                cotacaoVenda
            FROM raw_cotacoes_usd
            ORDER BY dataHoraCotacao DESC
            LIMIT 10
        """
    },
    "4": {
        "nome": "Estatísticas gerais",
        "sql": """
            SELECT 
                COUNT(*) as total_registros,
                ROUND(MIN(cotacaoCompra), 4) as menor_cotacao,
                ROUND(MAX(cotacaoCompra), 4) as maior_cotacao,
                ROUND(AVG(cotacaoCompra), 4) as media_cotacao
            FROM raw_cotacoes_usd
        """
    },
    "5": {
        "nome": "Cotações agrupadas por dia",
        "sql": """
            SELECT 
                DATE(dataHoraCotacao) as data,
                COUNT(*) as num_cotacoes,
                ROUND(AVG(cotacaoCompra), 4) as media_compra,
                ROUND(AVG(cotacaoVenda), 4) as media_venda
            FROM raw_cotacoes_usd
            GROUP BY DATE(dataHoraCotacao)
            ORDER BY data DESC
            LIMIT 10
        """
    },
    "6": {
        "nome": "Dias com maior variação",
        "sql": """
            SELECT 
                DATE(dataHoraCotacao) as data,
                ROUND(MAX(cotacaoCompra) - MIN(cotacaoCompra), 4) as variacao_dia
            FROM raw_cotacoes_usd
            GROUP BY DATE(dataHoraCotacao)
            ORDER BY variacao_dia DESC
            LIMIT 5
        """
    }
}

# Mostrar menu
for key, query in queries.items():
    print(f"  [{key}] {query['nome']}")

print()
print("="*80)
print()

# Pedir escolha do usuário
escolha = input("Digite o número da consulta (ou 'q' para sair): ").strip()

if escolha.lower() == 'q':
    print("\n👋 Até logo!")
    conn.close()
    sys.exit(0)

if escolha in queries:
    query_escolhida = queries[escolha]
    print()
    print(f"🔍 Executando: {query_escolhida['nome']}")
    print()
    print("📝 SQL:")
    print(query_escolhida['sql'])
    print()
    print("="*80)
    print()
    
    # Executar query
    try:
        resultado = conn.execute(query_escolhida['sql']).fetchdf()
        print(resultado.to_string(index=False))
        print()
        print(f"✅ {len(resultado)} linha(s) retornada(s)")
    except Exception as e:
        print(f"❌ Erro ao executar query: {e}")
else:
    print("❌ Opção inválida!")

print()
conn.close()