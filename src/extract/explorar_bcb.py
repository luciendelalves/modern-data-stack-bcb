"""
Script para explorar a API do Banco Central do Brasil
Vamos puxar dados de câmbio (dólar) como exemplo
"""

import requests
import json
from datetime import datetime, timedelta

print("🏦 EXPLORANDO A API DO BANCO CENTRAL\n")

# URL base da API de câmbio (PTAX = taxa de câmbio oficial)
base_url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata"

# Vamos pegar cotação do dólar dos últimos 7 dias
data_fim = datetime.now()
data_inicio = data_fim - timedelta(days=7)

# Formatar datas no formato que a API espera (MM-DD-YYYY)
data_inicio_str = data_inicio.strftime("%m-%d-%Y")
data_fim_str = data_fim.strftime("%m-%d-%Y")

print(f"📅 Buscando dados de {data_inicio_str} até {data_fim_str}\n")

# Montar a URL da requisição
# Estamos pedindo: cotações de compra e venda do dólar (moeda 220)
url = f"{base_url}/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
url += f"?@moeda='USD'&@dataInicial='{data_inicio_str}'&@dataFinalCotacao='{data_fim_str}'"
url += "&$format=json"

print("🔗 URL da requisição:")
print(url)
print("\n" + "="*80 + "\n")

try:
    # Fazer a requisição (é aqui que "ligamos" pro Banco Central)
    print("⏳ Fazendo requisição para o Banco Central...")
    response = requests.get(url, timeout=10)
    
    # Verificar se deu certo (código 200 = sucesso)
    if response.status_code == 200:
        print("✅ Sucesso! Dados recebidos.\n")
        
        # Converter resposta de JSON (texto) para dicionário Python
        dados = response.json()
        
        # A API retorna os dados dentro de 'value'
        cotacoes = dados.get('value', [])
        
        print(f"📊 Encontramos {len(cotacoes)} registros de cotação:\n")
        
        # Mostrar as primeiras 5 cotações
        for i, cotacao in enumerate(cotacoes[:5], 1):
            data = cotacao.get('dataHoraCotacao', 'N/A')
            compra = cotacao.get('cotacaoCompra', 'N/A')
            venda = cotacao.get('cotacaoVenda', 'N/A')
            
            print(f"  {i}. Data: {data}")
            print(f"     💵 Compra: R$ {compra}")
            print(f"     💰 Venda: R$ {venda}")
            print()
        
        if len(cotacoes) > 5:
            print(f"  ... e mais {len(cotacoes) - 5} registros\n")
        
        # Mostrar estrutura completa do primeiro registro
        print("="*80)
        print("\n🔍 ESTRUTURA COMPLETA DO PRIMEIRO REGISTRO:\n")
        print(json.dumps(cotacoes[0], indent=2, ensure_ascii=False))
        
    else:
        print(f"❌ Erro: Servidor retornou código {response.status_code}")
        print(f"Mensagem: {response.text[:200]}")

except requests.exceptions.Timeout:
    print("❌ Erro: Requisição demorou muito (timeout)")
except requests.exceptions.RequestException as e:
    print(f"❌ Erro na requisição: {e}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")

print("\n" + "="*80)
print("\n💡 PRÓXIMO PASSO: Vamos salvar esses dados no DuckDB!")
