#!/usr/bin/env python3
"""
Script de instalação e configuração do Sistema de Busca de Credenciados
"""

import subprocess
import sys
import os

def instalar_dependencias():
    """Instala as dependências necessárias"""
    print("Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def criar_dados_exemplo():
    """Cria dados de exemplo"""
    print("Criando dados de exemplo...")
    try:
        subprocess.check_call([sys.executable, "criar_dados_exemplo.py"])
        print("✅ Dados de exemplo criados com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar dados de exemplo: {e}")
        return False

def verificar_arquivos():
    """Verifica se os arquivos necessários existem"""
    arquivos_necessarios = [
        "app.py",
        "requirements.txt",
        "README.md",
        "config.json"
    ]
    
    print("Verificando arquivos...")
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")
            return False
    return True

def main():
    """Função principal do setup"""
    print("=" * 50)
    print("SISTEMA DE BUSCA DE CREDENCIADOS - SETUP")
    print("=" * 50)
    
    # Verificar arquivos
    if not verificar_arquivos():
        print("\n❌ Alguns arquivos necessários não foram encontrados.")
        return
    
    # Instalar dependências
    if not instalar_dependencias():
        print("\n❌ Falha na instalação das dependências.")
        return
    
    # Criar dados de exemplo
    if not criar_dados_exemplo():
        print("\n❌ Falha na criação dos dados de exemplo.")
        return
    
    print("\n" + "=" * 50)
    print("✅ SETUP CONCLUÍDO COM SUCESSO!")
    print("=" * 50)
    print("\nPara executar o sistema:")
    print("python app.py")
    print("\nPara mais informações, consulte o README.md")

if __name__ == "__main__":
    main() 