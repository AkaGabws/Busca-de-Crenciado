
import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd 
import folium 
import webbrowser
import os
from PIL import Image, ImageTk
import math



def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371  
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(math.radians(lat1)) * 
         math.cos(math.radians(lat2)) * 
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def gerar_mapa_com_rotas():
    cidade_cliente1 = entrada_cliente1.get()
    cidade1_data = df_cidades[df_cidades['nome'] == cidade_cliente1]
    if cidade1_data.empty:
        resultado_label.config(text="Cidade 1 não encontrada!")
        return
    lat1 = cidade1_data['LATITUDE'].values[0]
    lon1 = cidade1_data['LONGITUDE'].values[0]

    cidade_cliente2 = entrada_cliente2.get()
    cidade2_data = df_cidades[df_cidades['nome'] == cidade_cliente2]
    if cidade2_data.empty:
        resultado_label.config(text="Cidade 2 não encontrada!")
        return
    lat2 = cidade2_data['LATITUDE'].values[0]
    lon2 = cidade2_data['LONGITUDE'].values[0]
    
    estados_selecionados = [listbox_estados.get(i) for i in listbox_estados.curselection()]

    if estados_selecionados:
        df_credenciados_filtrados = df_credenciados[df_credenciados['UF'].isin(estados_selecionados)]
    else:
        df_credenciados_filtrados = df_credenciados

    if df_credenciados_filtrados.empty:
        resultado_label.config(text="Nenhum credenciado encontrado para os estados selecionados.")
        return

    
    df_credenciados_filtrados['distancia1'] = df_credenciados_filtrados.apply(
        lambda row: calcular_distancia(lat1, lon1, row['LATITUDE'], row['LONGITUDE']), axis=1
    )
    cidade_credenciada_mais_proxima1 = df_credenciados_filtrados.loc[df_credenciados_filtrados['distancia1'].idxmin()]
    lat_credenciado1 = cidade_credenciada_mais_proxima1['LATITUDE']
    lon_credenciado1 = cidade_credenciada_mais_proxima1['LONGITUDE']

    
    df_credenciados_filtrados['distancia2'] = df_credenciados_filtrados.apply(
        lambda row: calcular_distancia(lat2, lon2, row['LATITUDE'], row['LONGITUDE']), axis=1
    )
    cidade_credenciada_mais_proxima2 = df_credenciados_filtrados.loc[df_credenciados_filtrados['distancia2'].idxmin()]
    lat_credenciado2 = cidade_credenciada_mais_proxima2['LATITUDE']
    lon_credenciado2 = cidade_credenciada_mais_proxima2['LONGITUDE']

    
    distancia1 = calcular_distancia(lat1, lon1, lat_credenciado1, lon_credenciado1)
    distancia2 = calcular_distancia(lat2, lon2, lat_credenciado2, lon_credenciado2)

    mapa = folium.Map(location=[(lat1 + lat2) / 2, (lon1 + lon2) / 2], zoom_start=7)

    folium.Marker(location=[lat1, lon1], popup=cidade_cliente1, icon=folium.Icon(color='red')).add_to(mapa)
    folium.Marker(location=[lat_credenciado1, lon_credenciado1], popup=cidade_credenciada_mais_proxima1['nome'], icon=folium.Icon(color='green')).add_to(mapa)
    folium.PolyLine(locations=[[lat1, lon1], [lat_credenciado1, lon_credenciado1]], color='purple', weight=2.5, opacity=0.8).add_to(mapa)

    folium.Marker(location=[lat2, lon2], popup=cidade_cliente2, icon=folium.Icon(color='blue')).add_to(mapa)
    folium.Marker(location=[lat_credenciado2, lon_credenciado2], popup=cidade_credenciada_mais_proxima2['nome'], icon=folium.Icon(color='green')).add_to(mapa)
    folium.PolyLine(locations=[[lat2, lon2], [lat_credenciado2, lon_credenciado2]], color='purple', weight=2.5, opacity=0.8).add_to(mapa)
    
    
    for _, row in df_credenciados_filtrados.iterrows():
        folium.Marker(location=[row['LATITUDE'], row['LONGITUDE']],
                      popup=row['nome'],
                      icon=folium.Icon(color='green')).add_to(mapa)

    
    folium.Marker(location=[(lat1 + lat2) / 2, (lon1 + lon2) / 2], 
                  popup=f'Distâncias: Cliente 1 a Credenciado: {distancia1:.2f} km, Cliente 2 a Credenciado: {distancia2:.2f} km', 
                  icon=folium.Icon(color='orange')).add_to(mapa)

    mapa.save('mapa_com_rotas.html')
    resultado_label.config(text="Mapa gerado com sucesso!")
    resultado_label.config(text=f"Mapa gerado com sucesso! Distância: {calcular_distancia(lat1, lon1, lat2, lon2):.2f} km.")


def abrir_mapa():
    if os.path.exists('mapa_com_rotas.html'):
        webbrowser.open('mapa_com_rotas.html')
    else:
        resultado_label.config(text="O arquivo do mapa não foi encontrado. Gere o mapa primeiro!")




try:
    df_cidades = pd.read_excel(r"L:\00_LOCALIZACAO CREDENCIADO\RELAÇÃO DE CIDADES.xlsx", sheet_name="Clientes")
    df_credenciados = pd.read_excel(r"L:\00_LOCALIZACAO CREDENCIADO\RELAÇÃO DE CIDADES.xlsx", sheet_name="Credenciados")
except Exception as e:
    print(f"Erro ao carregar planilhas: {e}")
    exit()

estados_disponiveis = df_credenciados['UF'].unique()
df_importada = None



root = tk.Tk()
root.title("Mapa Engemed")
root.geometry("500x500")
root.configure(bg='#f0f0f0')


img = Image.open(r"L:\09_MKT\LOGO ENGEMED\LOGO SEM FUNDO ENGEMED.png")
img = img.resize((100, 50), Image.LANCZOS)
logo_img = ImageTk.PhotoImage(img)
logo_label = tk.Label(root, image=logo_img, bg='#f0f0f0')
logo_label.place(x=10, y=10)


frame_central = tk.Frame(root, bg='#f0f0f0')
frame_central.place(relx=0.5, rely=0.35, anchor=tk.CENTER)


label_cliente1 = tk.Label(frame_central, text="Cidade do Cliente 1", bg='#f0f0f0')
label_cliente1.grid(row=0, column=0, padx=10, pady=5, sticky='e')
entrada_cliente1 = ttk.Combobox(frame_central, values=df_cidades['nome'].unique(), width=30)
entrada_cliente1.grid(row=0, column=1, padx=10, pady=5, sticky='w')


label_cliente2 = tk.Label(frame_central, text="Cidade do Cliente 2", bg='#f0f0f0')
label_cliente2.grid(row=1, column=0, padx=10, pady=5, sticky='e')
entrada_cliente2 = ttk.Combobox(frame_central, values=df_cidades['nome'].unique(), width=30)
entrada_cliente2.grid(row=1, column=1, padx=10, pady=5, sticky='w')


label_estados = tk.Label(frame_central, text="Estados (selecione vários)", bg='#f0f0f0')
label_estados.grid(row=2, column=0, padx=10, pady=5, sticky='e')
listbox_estados = tk.Listbox(frame_central, selectmode='multiple', height=4)
for estado in estados_disponiveis:
    listbox_estados.insert(tk.END, estado)
listbox_estados.grid(row=2, column=1, padx=10, pady=5, sticky='w')


botao_gerar_mapa = tk.Button(frame_central, text="Gerar Mapa", command=gerar_mapa_com_rotas)
botao_gerar_mapa.grid(row=3, columnspan=2, pady=10)


botao_abrir_mapa = tk.Button(frame_central, text="Abrir Mapa", command=abrir_mapa)
botao_abrir_mapa.grid(row=4, columnspan=2, pady=10)


resultado_label = tk.Label(root, text="", bg='#f0f0f0')
resultado_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

root.mainloop()
