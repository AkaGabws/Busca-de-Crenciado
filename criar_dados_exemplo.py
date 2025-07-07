import pandas as pd
import numpy as np

def criar_dados_exemplo():
    """Cria dados de exemplo para teste do sistema"""
    
    # Dados de clientes (cidades brasileiras)
    clientes_data = {
        'nome': [
            'São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Brasília',
            'Fortaleza', 'Curitiba', 'Manaus', 'Recife', 'Porto Alegre',
            'Belém', 'Goiânia', 'Guarulhos', 'Campinas', 'São Luís'
        ],
        'LATITUDE': [
            -23.5505, -22.9068, -19.9167, -12.9714, -15.7942,
            -3.7319, -25.4284, -3.1190, -8.0476, -30.0346,
            -1.4554, -16.6864, -23.4543, -22.9064, -2.5297
        ],
        'LONGITUDE': [
            -46.6333, -43.1729, -43.9345, -38.5014, -47.8822,
            -38.5267, -49.2733, -60.0217, -34.8770, -51.2177,
            -48.4898, -49.2653, -46.5336, -47.0616, -44.3028
        ]
    }
    
    # Dados de credenciados (hospitais e clínicas)
    credenciados_data = {
        'nome': [
            'Hospital Albert Einstein', 'Hospital Sírio-Libanês', 'Hospital das Clínicas',
            'Hospital Samaritano', 'Hospital Alemão Oswaldo Cruz', 'Hospital Beneficência Portuguesa',
            'Hospital Santa Catarina', 'Hospital São Camilo', 'Hospital 9 de Julho',
            'Hospital do Coração', 'Hospital Israelita Albert Einstein', 'Hospital Moinhos de Vento',
            'Hospital de Clínicas de Porto Alegre', 'Hospital São Lucas', 'Hospital Mãe de Deus',
            'Hospital Ernesto Dornelles', 'Hospital Conceição', 'Hospital de Clínicas',
            'Hospital Universitário', 'Hospital de Base', 'Hospital Regional', 'Hospital Municipal',
            'Clínica São Vicente', 'Clínica Santa Maria', 'Clínica São José', 'Clínica Santa Rita',
            'Centro Médico ABC', 'Centro Médico XYZ', 'Centro Médico 123', 'Centro Médico Saúde'
        ],
        'UF': [
            'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP',
            'SP', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'PR', 'PR', 'DF',
            'DF', 'DF', 'MG', 'MG', 'MG', 'MG', 'RJ', 'RJ', 'RJ', 'RJ'
        ],
        'LATITUDE': [
            -23.5505, -23.5605, -23.5705, -23.5805, -23.5905,
            -23.6005, -23.6105, -23.6205, -23.6305, -23.6405,
            -23.6505, -30.0346, -30.0446, -30.0546, -30.0646,
            -30.0746, -30.0846, -25.4284, -25.4384, -15.7942,
            -15.8042, -15.8142, -19.9167, -19.9267, -19.9367,
            -19.9467, -22.9068, -22.9168, -22.9268, -22.9368
        ],
        'LONGITUDE': [
            -46.6333, -46.6433, -46.6533, -46.6633, -46.6733,
            -46.6833, -46.6933, -46.7033, -46.7133, -46.7233,
            -46.7333, -51.2177, -51.2277, -51.2377, -51.2477,
            -51.2577, -51.2677, -49.2733, -49.2833, -47.8822,
            -47.8922, -47.9022, -43.9345, -43.9445, -43.9545,
            -43.9645, -43.1729, -43.1829, -43.1929, -43.2029
        ]
    }
    
    # Criar DataFrames
    df_clientes = pd.DataFrame(clientes_data)
    df_credenciados = pd.DataFrame(credenciados_data)
    
    # Salvar em arquivo Excel
    with pd.ExcelWriter('dados_credenciados.xlsx', engine='openpyxl') as writer:
        df_clientes.to_excel(writer, sheet_name='Clientes', index=False)
        df_credenciados.to_excel(writer, sheet_name='Credenciados', index=False)
    
    print("Dados de exemplo criados com sucesso!")
    print(f"Clientes: {len(df_clientes)} registros")
    print(f"Credenciados: {len(df_credenciados)} registros")
    print("Arquivo: dados_credenciados.xlsx")

if __name__ == "__main__":
    criar_dados_exemplo() 