import sqlite3
import pandas as pd
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="credenciados.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Criar tabela de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Criar tabela de credenciados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credenciados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                uf TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Criar tabela de mapas gerados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mapas_gerados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_arquivo TEXT NOT NULL,
                cliente1_id INTEGER,
                cliente2_id INTEGER,
                estados_filtro TEXT,
                data_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente1_id) REFERENCES clientes (id),
                FOREIGN KEY (cliente2_id) REFERENCES clientes (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def inserir_cliente(self, nome, latitude, longitude):
        """Insere um novo cliente no banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clientes (nome, latitude, longitude)
            VALUES (?, ?, ?)
        ''', (nome, latitude, longitude))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def inserir_credenciado(self, nome, uf, latitude, longitude):
        """Insere um novo credenciado no banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO credenciados (nome, uf, latitude, longitude)
            VALUES (?, ?, ?, ?)
        ''', (nome, uf, latitude, longitude))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def buscar_clientes(self):
        """Retorna todos os clientes"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('SELECT * FROM clientes ORDER BY nome', conn)
        conn.close()
        return df
    
    def buscar_credenciados(self, uf=None):
        """Retorna credenciados, opcionalmente filtrados por UF"""
        conn = sqlite3.connect(self.db_path)
        
        if uf:
            df = pd.read_sql_query('''
                SELECT * FROM credenciados 
                WHERE uf = ? 
                ORDER BY nome
            ''', conn, params=[uf])
        else:
            df = pd.read_sql_query('SELECT * FROM credenciados ORDER BY nome', conn)
        
        conn.close()
        return df
    
    def buscar_estados(self):
        """Retorna lista de estados únicos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT uf FROM credenciados ORDER BY uf')
        estados = [row[0] for row in cursor.fetchall()]
        conn.close()
        return estados
    
    def buscar_cliente_por_id(self, cliente_id):
        """Busca cliente específico por ID"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('SELECT * FROM clientes WHERE id = ?', conn, params=[cliente_id])
        conn.close()
        return df.iloc[0] if not df.empty else None
    
    def buscar_credenciado_por_id(self, credenciado_id):
        """Busca credenciado específico por ID"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('SELECT * FROM credenciados WHERE id = ?', conn, params=[credenciado_id])
        conn.close()
        return df.iloc[0] if not df.empty else None
    
    def salvar_mapa_gerado(self, nome_arquivo, cliente1_id, cliente2_id, estados_filtro):
        """Salva registro de mapa gerado"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO mapas_gerados (nome_arquivo, cliente1_id, cliente2_id, estados_filtro)
            VALUES (?, ?, ?, ?)
        ''', (nome_arquivo, cliente1_id, cliente2_id, estados_filtro))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def buscar_historico_mapas(self):
        """Retorna histórico de mapas gerados"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('''
            SELECT m.*, 
                   c1.nome as cliente1_nome,
                   c2.nome as cliente2_nome
            FROM mapas_gerados m
            LEFT JOIN clientes c1 ON m.cliente1_id = c1.id
            LEFT JOIN clientes c2 ON m.cliente2_id = c2.id
            ORDER BY m.data_geracao DESC
        ''', conn)
        conn.close()
        return df
    
    def importar_dados_excel(self, arquivo_excel):
        """Importa dados de arquivo Excel para o banco"""
        try:
            # Ler dados do Excel
            df_clientes = pd.read_excel(arquivo_excel, sheet_name="Clientes")
            df_credenciados = pd.read_excel(arquivo_excel, sheet_name="Credenciados")
            
            # Limpar tabelas existentes
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM clientes')
            cursor.execute('DELETE FROM credenciados')
            conn.commit()
            conn.close()
            
            # Inserir clientes
            for _, row in df_clientes.iterrows():
                self.inserir_cliente(row['nome'], row['LATITUDE'], row['LONGITUDE'])
            
            # Inserir credenciados
            for _, row in df_credenciados.iterrows():
                self.inserir_credenciado(row['nome'], row['UF'], row['LATITUDE'], row['LONGITUDE'])
            
            return True, f"Importados {len(df_clientes)} clientes e {len(df_credenciados)} credenciados"
            
        except Exception as e:
            return False, f"Erro ao importar dados: {str(e)}"
    
    def criar_dados_exemplo(self):
        """Cria dados de exemplo no banco"""
        # Dados de clientes
        clientes_exemplo = [
            ('São Paulo', -23.5505, -46.6333),
            ('Rio de Janeiro', -22.9068, -43.1729),
            ('Belo Horizonte', -19.9167, -43.9345),
            ('Salvador', -12.9714, -38.5014),
            ('Brasília', -15.7942, -47.8822),
            ('Fortaleza', -3.7319, -38.5267),
            ('Curitiba', -25.4284, -49.2733),
            ('Manaus', -3.1190, -60.0217),
            ('Recife', -8.0476, -34.8770),
            ('Porto Alegre', -30.0346, -51.2177)
        ]
        
        # Dados de credenciados
        credenciados_exemplo = [
            ('Hospital Albert Einstein', 'SP', -23.5505, -46.6333),
            ('Hospital Sírio-Libanês', 'SP', -23.5605, -46.6433),
            ('Hospital das Clínicas', 'SP', -23.5705, -46.6533),
            ('Hospital Samaritano', 'SP', -23.5805, -46.6633),
            ('Hospital Alemão Oswaldo Cruz', 'SP', -23.5905, -46.6733),
            ('Hospital Moinhos de Vento', 'RS', -30.0346, -51.2177),
            ('Hospital de Clínicas de Porto Alegre', 'RS', -30.0446, -51.2277),
            ('Hospital São Lucas', 'RS', -30.0546, -51.2377),
            ('Hospital Mãe de Deus', 'RS', -30.0646, -51.2477),
            ('Hospital de Clínicas', 'PR', -25.4284, -49.2733),
            ('Hospital Universitário', 'PR', -25.4384, -49.2833),
            ('Hospital de Base', 'DF', -15.7942, -47.8822),
            ('Hospital Regional', 'DF', -15.8042, -47.8922),
            ('Hospital Municipal', 'DF', -15.8142, -47.9022),
            ('Clínica São Vicente', 'MG', -19.9167, -43.9345),
            ('Clínica Santa Maria', 'MG', -19.9267, -43.9445),
            ('Clínica São José', 'MG', -19.9367, -43.9545),
            ('Centro Médico ABC', 'RJ', -22.9068, -43.1729),
            ('Centro Médico XYZ', 'RJ', -22.9168, -43.1829),
            ('Centro Médico 123', 'RJ', -22.9268, -43.1929)
        ]
        
        # Limpar dados existentes
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM clientes')
        cursor.execute('DELETE FROM credenciados')
        conn.commit()
        conn.close()
        
        # Inserir dados de exemplo
        for nome, lat, lon in clientes_exemplo:
            self.inserir_cliente(nome, lat, lon)
        
        for nome, uf, lat, lon in credenciados_exemplo:
            self.inserir_credenciado(nome, uf, lat, lon)
        
        return len(clientes_exemplo), len(credenciados_exemplo) 