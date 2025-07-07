from flask import Flask, render_template, request, jsonify, send_file
from database import DatabaseManager
import folium
import math
import os
from datetime import datetime
import json
import pandas as pd

app = Flask(__name__)
db = DatabaseManager()

# Configurações
app.config['SECRET_KEY'] = 'engemed_credenciados_2024'
app.config['UPLOAD_FOLDER'] = 'static/mapas'

# Criar pasta para mapas se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def calcular_distancia(lat1, lon1, lat2, lon2):
    """Calcula distância entre dois pontos usando fórmula de Haversine"""
    R = 6371  # Raio da Terra em km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(math.radians(lat1)) * 
         math.cos(math.radians(lat2)) * 
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/clientes')
def api_clientes():
    """API para buscar clientes"""
    try:
        clientes = db.buscar_clientes()
        return jsonify({
            'success': True,
            'data': clientes.to_dict('records')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/estados')
def api_estados():
    """API para buscar estados"""
    try:
        estados = db.buscar_estados()
        return jsonify({
            'success': True,
            'data': estados
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/credenciados')
def api_credenciados():
    """API para buscar credenciados"""
    try:
        uf = request.args.get('uf')
        credenciados = db.buscar_credenciados(uf)
        return jsonify({
            'success': True,
            'data': credenciados.to_dict('records')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/gerar-mapa', methods=['POST'])
def api_gerar_mapa():
    """API para gerar mapa"""
    try:
        data = request.get_json()
        cliente1_id = data.get('cliente1_id')
        cliente2_id = data.get('cliente2_id')
        estados_filtro = data.get('estados_filtro', [])
        
        # Buscar dados dos clientes
        cliente1 = db.buscar_cliente_por_id(cliente1_id)
        cliente2 = db.buscar_cliente_por_id(cliente2_id)
        
        # Correção: checar se é None ou se é Series/DataFrame vazio
        if cliente1 is None or cliente2 is None:
            return jsonify({
                'success': False,
                'error': 'Cliente não encontrado'
            })
        if hasattr(cliente1, 'empty') and cliente1.empty:
            return jsonify({
                'success': False,
                'error': 'Cliente 1 não encontrado'
            })
        if hasattr(cliente2, 'empty') and cliente2.empty:
            return jsonify({
                'success': False,
                'error': 'Cliente 2 não encontrado'
            })
        
        # Buscar credenciados filtrados
        if estados_filtro:
            credenciados_filtrados = []
            for uf in estados_filtro:
                cred_uf = db.buscar_credenciados(uf)
                if not cred_uf.empty:
                    credenciados_filtrados.append(cred_uf)
            if credenciados_filtrados:
                df_credenciados = pd.concat(credenciados_filtrados, ignore_index=True)
            else:
                df_credenciados = pd.DataFrame()
        else:
            df_credenciados = db.buscar_credenciados()
        
        if df_credenciados.empty:
            return jsonify({
                'success': False,
                'error': 'Nenhum credenciado encontrado para os estados selecionados'
            })
        
        # Calcular distâncias
        df_credenciados['distancia1'] = df_credenciados.apply(
            lambda row: calcular_distancia(
                cliente1['latitude'], cliente1['longitude'], 
                row['latitude'], row['longitude']
            ), axis=1
        )
        
        df_credenciados['distancia2'] = df_credenciados.apply(
            lambda row: calcular_distancia(
                cliente2['latitude'], cliente2['longitude'], 
                row['latitude'], row['longitude']
            ), axis=1
        )
        
        # Encontrar credenciados mais próximos
        credenciado1 = df_credenciados.loc[df_credenciados['distancia1'].idxmin()]
        credenciado2 = df_credenciados.loc[df_credenciados['distancia2'].idxmin()]
        
        # Criar mapa
        mapa = folium.Map(
            location=[(cliente1['latitude'] + cliente2['latitude']) / 2, 
                     (cliente1['longitude'] + cliente2['longitude']) / 2], 
            zoom_start=7
        )
        
        # Adicionar marcadores dos clientes
        folium.Marker(
            location=[cliente1['latitude'], cliente1['longitude']], 
            popup=f"Cliente 1: {cliente1['nome']}", 
            icon=folium.Icon(color='red', icon='user')
        ).add_to(mapa)
        
        folium.Marker(
            location=[cliente2['latitude'], cliente2['longitude']], 
            popup=f"Cliente 2: {cliente2['nome']}", 
            icon=folium.Icon(color='blue', icon='user')
        ).add_to(mapa)
        
        # Adicionar credenciados mais próximos
        folium.Marker(
            location=[credenciado1['latitude'], credenciado1['longitude']], 
            popup=f"Credenciado 1: {credenciado1['nome']}<br>Distância: {credenciado1['distancia1']:.2f} km", 
            icon=folium.Icon(color='green', icon='hospital-o')
        ).add_to(mapa)
        
        folium.Marker(
            location=[credenciado2['latitude'], credenciado2['longitude']], 
            popup=f"Credenciado 2: {credenciado2['nome']}<br>Distância: {credenciado2['distancia2']:.2f} km", 
            icon=folium.Icon(color='green', icon='hospital-o')
        ).add_to(mapa)
        
        # Adicionar rotas
        folium.PolyLine(
            locations=[[cliente1['latitude'], cliente1['longitude']], 
                      [credenciado1['latitude'], credenciado1['longitude']]], 
            color='purple', weight=3, opacity=0.8
        ).add_to(mapa)
        
        folium.PolyLine(
            locations=[[cliente2['latitude'], cliente2['longitude']], 
                      [credenciado2['latitude'], credenciado2['longitude']]], 
            color='purple', weight=3, opacity=0.8
        ).add_to(mapa)
        
        # Adicionar todos os credenciados filtrados
        for _, row in df_credenciados.iterrows():
            folium.Marker(
                location=[float(row['latitude']), float(row['longitude'])],
                popup=f"{row['nome']}<br>UF: {row['uf']}",
                icon=folium.Icon(color='lightgreen', icon='info-sign')
            ).add_to(mapa)
        
        # Salvar mapa
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"mapa_credenciados_{timestamp}.html"
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
        mapa.save(caminho_arquivo)
        
        # Salvar no banco
        db.salvar_mapa_gerado(nome_arquivo, cliente1_id, cliente2_id, ','.join(estados_filtro))
        
        return jsonify({
            'success': True,
            'arquivo': nome_arquivo,
            'distancias': {
                'cliente1_credenciado1': round(credenciado1['distancia1'], 2),
                'cliente2_credenciado2': round(credenciado2['distancia2'], 2)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/historico')
def api_historico():
    """API para buscar histórico de mapas"""
    try:
        historico = db.buscar_historico_mapas()
        return jsonify({
            'success': True,
            'data': historico.to_dict('records')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/importar-excel', methods=['POST'])
def api_importar_excel():
    """API para importar dados do Excel"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo enviado'
            })
        
        arquivo = request.files['file']
        if arquivo.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo selecionado'
            })
        
        # Salvar arquivo temporariamente
        caminho_temp = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        arquivo.save(caminho_temp)
        
        # Importar dados
        success, message = db.importar_dados_excel(caminho_temp)
        
        # Remover arquivo temporário
        os.remove(caminho_temp)
        
        return jsonify({
            'success': success,
            'message': message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/criar-dados-exemplo')
def api_criar_dados_exemplo():
    """API para criar dados de exemplo"""
    try:
        num_clientes, num_credenciados = db.criar_dados_exemplo()
        return jsonify({
            'success': True,
            'message': f'Dados de exemplo criados: {num_clientes} clientes e {num_credenciados} credenciados'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/mapa/<nome_arquivo>')
def visualizar_mapa(nome_arquivo):
    """Rota para visualizar mapa específico"""
    caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
    if os.path.exists(caminho_arquivo):
        return send_file(caminho_arquivo)
    else:
        return "Mapa não encontrado", 404

if __name__ == '__main__':
    # Criar dados de exemplo se o banco estiver vazio
    clientes = db.buscar_clientes()
    if clientes.empty:
        print("Criando dados de exemplo...")
        db.criar_dados_exemplo()
    
    print("Iniciando servidor Flask...")
    print("Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 