#!/usr/bin/env python3
"""
Script de teste para a versão web do Sistema de Busca de Credenciados
"""

import requests
import json
import time
import sys

class TesteWeb:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def testar_conexao(self):
        """Testa se o servidor está rodando"""
        print("🔍 Testando conexão com o servidor...")
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("✅ Servidor está rodando")
                return True
            else:
                print(f"❌ Servidor retornou status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Não foi possível conectar ao servidor")
            print("   Certifique-se de que a aplicação está rodando com: python app_web.py")
            return False
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def testar_api_clientes(self):
        """Testa a API de clientes"""
        print("\n👥 Testando API de clientes...")
        try:
            response = self.session.get(f"{self.base_url}/api/clientes")
            data = response.json()
            
            if data['success']:
                print(f"✅ API de clientes funcionando - {len(data['data'])} clientes encontrados")
                return True
            else:
                print(f"❌ Erro na API de clientes: {data.get('error', 'Erro desconhecido')}")
                return False
        except Exception as e:
            print(f"❌ Erro ao testar API de clientes: {e}")
            return False
    
    def testar_api_estados(self):
        """Testa a API de estados"""
        print("\n🗺️ Testando API de estados...")
        try:
            response = self.session.get(f"{self.base_url}/api/estados")
            data = response.json()
            
            if data['success']:
                print(f"✅ API de estados funcionando - {len(data['data'])} estados encontrados")
                return True
            else:
                print(f"❌ Erro na API de estados: {data.get('error', 'Erro desconhecido')}")
                return False
        except Exception as e:
            print(f"❌ Erro ao testar API de estados: {e}")
            return False
    
    def testar_criar_dados_exemplo(self):
        """Testa a criação de dados de exemplo"""
        print("\n📊 Testando criação de dados de exemplo...")
        try:
            response = self.session.get(f"{self.base_url}/api/criar-dados-exemplo")
            data = response.json()
            
            if data['success']:
                print(f"✅ Dados de exemplo criados: {data['message']}")
                return True
            else:
                print(f"❌ Erro ao criar dados: {data.get('error', 'Erro desconhecido')}")
                return False
        except Exception as e:
            print(f"❌ Erro ao testar criação de dados: {e}")
            return False
    
    def testar_gerar_mapa(self):
        """Testa a geração de mapa"""
        print("\n🗺️ Testando geração de mapa...")
        try:
            # Primeiro, buscar clientes disponíveis
            response_clientes = self.session.get(f"{self.base_url}/api/clientes")
            clientes_data = response_clientes.json()
            
            if not clientes_data['success'] or len(clientes_data['data']) < 2:
                print("❌ Não há clientes suficientes para testar")
                return False
            
            # Pegar os dois primeiros clientes
            cliente1 = clientes_data['data'][0]
            cliente2 = clientes_data['data'][1]
            
            # Gerar mapa
            payload = {
                'cliente1_id': cliente1['id'],
                'cliente2_id': cliente2['id'],
                'estados_filtro': []
            }
            
            response = self.session.post(
                f"{self.base_url}/api/gerar-mapa",
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            
            data = response.json()
            
            if data['success']:
                print(f"✅ Mapa gerado com sucesso: {data['arquivo']}")
                print(f"   Distâncias: Cliente 1 → {data['distancias']['cliente1_credenciado1']} km, Cliente 2 → {data['distancias']['cliente2_credenciado2']} km")
                return True
            else:
                print(f"❌ Erro ao gerar mapa: {data.get('error', 'Erro desconhecido')}")
                return False
        except Exception as e:
            print(f"❌ Erro ao testar geração de mapa: {e}")
            return False
    
    def testar_api_historico(self):
        """Testa a API de histórico"""
        print("\n📋 Testando API de histórico...")
        try:
            response = self.session.get(f"{self.base_url}/api/historico")
            data = response.json()
            
            if data['success']:
                print(f"✅ API de histórico funcionando - {len(data['data'])} registros encontrados")
                return True
            else:
                print(f"❌ Erro na API de histórico: {data.get('error', 'Erro desconhecido')}")
                return False
        except Exception as e:
            print(f"❌ Erro ao testar API de histórico: {e}")
            return False
    
    def testar_interface_web(self):
        """Testa se a interface web está acessível"""
        print("\n🌐 Testando interface web...")
        try:
            response = self.session.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                if "Sistema de Busca de Credenciados" in response.text:
                    print("✅ Interface web carregada corretamente")
                    return True
                else:
                    print("❌ Interface web não contém conteúdo esperado")
                    return False
            else:
                print(f"❌ Interface web retornou status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro ao testar interface web: {e}")
            return False
    
    def executar_todos_testes(self):
        """Executa todos os testes"""
        print("=" * 60)
        print("🧪 TESTE DA VERSÃO WEB - SISTEMA DE CREDENCIADOS")
        print("=" * 60)
        
        testes = [
            ("Conexão", self.testar_conexao),
            ("Interface Web", self.testar_interface_web),
            ("API Clientes", self.testar_api_clientes),
            ("API Estados", self.testar_api_estados),
            ("Criar Dados Exemplo", self.testar_criar_dados_exemplo),
            ("Gerar Mapa", self.testar_gerar_mapa),
            ("API Histórico", self.testar_api_historico)
        ]
        
        resultados = []
        for nome, teste in testes:
            try:
                resultado = teste()
                resultados.append((nome, resultado))
            except Exception as e:
                print(f"❌ Erro no teste {nome}: {e}")
                resultados.append((nome, False))
        
        print("\n" + "=" * 60)
        print("📋 RESUMO DOS TESTES")
        print("=" * 60)
        
        todos_ok = True
        for nome, resultado in resultados:
            status = "✅ PASSOU" if resultado else "❌ FALHOU"
            print(f"{nome}: {status}")
            if not resultado:
                todos_ok = False
        
        print("\n" + "=" * 60)
        if todos_ok:
            print("🎉 TODOS OS TESTES PASSARAM!")
            print("✅ A versão web está funcionando perfeitamente!")
            print(f"\n🌐 Acesse: {self.base_url}")
        else:
            print("⚠️  ALGUNS TESTES FALHARAM!")
            print("❌ Verifique os erros acima antes de usar o sistema")
        print("=" * 60)

def main():
    """Função principal"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:5000"
    
    teste = TesteWeb(base_url)
    teste.executar_todos_testes()

if __name__ == "__main__":
    main() 