#!/usr/bin/env python3
"""
Script de teste para verificar se o sistema está funcionando corretamente
"""

import pandas as pd
import os
import sys

def testar_importacoes():
    """Testa se todas as dependências estão instaladas"""
    print("🔍 Testando importações...")
    
    try:
        import tkinter
        print("✅ tkinter - OK")
    except ImportError:
        print("❌ tkinter - FALHOU")
        return False
    
    try:
        import pandas
        print("✅ pandas - OK")
    except ImportError:
        print("❌ pandas - FALHOU")
        return False
    
    try:
        import folium
        print("✅ folium - OK")
    except ImportError:
        print("❌ folium - FALHOU")
        return False
    
    try:
        from PIL import Image
        print("✅ PIL (Pillow) - OK")
    except ImportError:
        print("❌ PIL (Pillow) - FALHOU")
        return False
    
    try:
        import openpyxl
        print("✅ openpyxl - OK")
    except ImportError:
        print("❌ openpyxl - FALHOU")
        return False
    
    return True

def testar_arquivos():
    """Testa se os arquivos necessários existem"""
    print("\n📁 Testando arquivos...")
    
    arquivos_necessarios = [
        "app.py",
        "dados_credenciados.xlsx",
        "config.json",
        "requirements.txt"
    ]
    
    todos_ok = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} - OK")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")
            todos_ok = False
    
    return todos_ok

def testar_dados():
    """Testa se os dados estão corretos"""
    print("\n📊 Testando dados...")
    
    try:
        # Carregar dados
        df_clientes = pd.read_excel("dados_credenciados.xlsx", sheet_name="Clientes")
        df_credenciados = pd.read_excel("dados_credenciados.xlsx", sheet_name="Credenciados")
        
        print(f"✅ Clientes carregados: {len(df_clientes)} registros")
        print(f"✅ Credenciados carregados: {len(df_credenciados)} registros")
        
        # Verificar colunas
        colunas_clientes = ['nome', 'LATITUDE', 'LONGITUDE']
        colunas_credenciados = ['nome', 'UF', 'LATITUDE', 'LONGITUDE']
        
        if all(col in df_clientes.columns for col in colunas_clientes):
            print("✅ Colunas dos clientes - OK")
        else:
            print("❌ Colunas dos clientes - FALHOU")
            return False
        
        if all(col in df_credenciados.columns for col in colunas_credenciados):
            print("✅ Colunas dos credenciados - OK")
        else:
            print("❌ Colunas dos credenciados - FALHOU")
            return False
        
        # Verificar se há dados
        if len(df_clientes) > 0 and len(df_credenciados) > 0:
            print("✅ Dados não vazios - OK")
        else:
            print("❌ Dados vazios - FALHOU")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar dados: {e}")
        return False

def testar_calculo_distancia():
    """Testa o cálculo de distância"""
    print("\n📏 Testando cálculo de distância...")
    
    try:
        import math
        
        def calcular_distancia(lat1, lon1, lat2, lon2):
            R = 6371  # Raio da Terra em km
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = (math.sin(dlat / 2) ** 2 + 
                 math.cos(math.radians(lat1)) * 
                 math.cos(math.radians(lat2)) * 
                 math.sin(dlon / 2) ** 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return R * c
        
        # Teste com coordenadas conhecidas (São Paulo para Rio de Janeiro)
        distancia = calcular_distancia(-23.5505, -46.6333, -22.9068, -43.1729)
        
        if 300 < distancia < 500:  # Distância aproximada entre SP e RJ
            print(f"✅ Cálculo de distância - OK ({distancia:.2f} km)")
            return True
        else:
            print(f"❌ Cálculo de distância - FALHOU (distância: {distancia:.2f} km)")
            return False
            
    except Exception as e:
        print(f"❌ Erro no cálculo de distância: {e}")
        return False

def main():
    """Função principal do teste"""
    print("=" * 60)
    print("🧪 TESTE DO SISTEMA DE BUSCA DE CREDENCIADOS")
    print("=" * 60)
    
    testes = [
        ("Importações", testar_importacoes),
        ("Arquivos", testar_arquivos),
        ("Dados", testar_dados),
        ("Cálculo de Distância", testar_calculo_distancia)
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
        print("✅ O sistema está pronto para uso!")
        print("\nPara executar: python app.py")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM!")
        print("❌ Verifique os erros acima antes de usar o sistema")
    print("=" * 60)

if __name__ == "__main__":
    main() 