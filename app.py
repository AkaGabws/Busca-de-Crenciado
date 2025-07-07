import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd 
import folium 
import webbrowser
import os
from PIL import Image, ImageTk
import math
import json
from datetime import datetime

class SistemaCredenciados:
    def __init__(self):
        self.df_cidades = None
        self.df_credenciados = None
        self.estados_disponiveis = []
        self.config = self.carregar_config()
        
        self.setup_interface()
        self.carregar_dados()
    
    def carregar_config(self):
        """Carrega configurações do arquivo config.json"""
        config_padrao = {
            "arquivo_dados": "dados_credenciados.xlsx",
            "logo_path": "logo.png",
            "cor_primaria": "#2E86AB",
            "cor_secundaria": "#A23B72",
            "cor_fundo": "#F8F9FA"
        }
        
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                with open("config.json", "w", encoding="utf-8") as f:
                    json.dump(config_padrao, f, indent=4, ensure_ascii=False)
                return config_padrao
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            return config_padrao
    
    def setup_interface(self):
        """Configura a interface gráfica"""
        self.root = tk.Tk()
        self.root.title("Sistema de Busca de Credenciados - Engemed")
        self.root.geometry("600x700")
        self.root.configure(bg=self.config["cor_fundo"])
        self.root.resizable(True, True)
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Carregar logo se existir
        self.carregar_logo()
        
        # Criar frames
        self.criar_frames()
        self.criar_widgets()
        self.criar_menu()
    
    def carregar_logo(self):
        """Carrega o logo da empresa"""
        try:
            if os.path.exists(self.config["logo_path"]):
                img = Image.open(self.config["logo_path"])
                img = img.resize((120, 60), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                self.logo_label = tk.Label(self.root, image=self.logo_img, bg=self.config["cor_fundo"])
                self.logo_label.place(x=10, y=10)
            else:
                # Criar logo placeholder
                self.logo_label = tk.Label(self.root, text="ENGEMED", 
                                         font=("Arial", 16, "bold"), 
                                         fg=self.config["cor_primaria"],
                                         bg=self.config["cor_fundo"])
                self.logo_label.place(x=10, y=10)
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
            self.logo_label = tk.Label(self.root, text="ENGEMED", 
                                     font=("Arial", 16, "bold"), 
                                     fg=self.config["cor_primaria"],
                                     bg=self.config["cor_fundo"])
            self.logo_label.place(x=10, y=10)
    
    def criar_frames(self):
        """Cria os frames da interface"""
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg=self.config["cor_fundo"])
        self.frame_principal.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=550, height=600)
        
        # Frame de título
        self.frame_titulo = tk.Frame(self.frame_principal, bg=self.config["cor_fundo"])
        self.frame_titulo.pack(fill=tk.X, pady=(0, 20))
        
        # Frame de entrada de dados
        self.frame_entrada = tk.Frame(self.frame_principal, bg=self.config["cor_fundo"])
        self.frame_entrada.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Frame de botões
        self.frame_botoes = tk.Frame(self.frame_principal, bg=self.config["cor_fundo"])
        self.frame_botoes.pack(fill=tk.X, pady=20)
        
        # Frame de status
        self.frame_status = tk.Frame(self.frame_principal, bg=self.config["cor_fundo"])
        self.frame_status.pack(fill=tk.X, pady=10)
    
    def criar_widgets(self):
        """Cria os widgets da interface"""
        # Título
        titulo = tk.Label(self.frame_titulo, text="Sistema de Busca de Credenciados", 
                         font=("Arial", 18, "bold"), 
                         fg=self.config["cor_primaria"],
                         bg=self.config["cor_fundo"])
        titulo.pack()
        
        # Cliente 1
        self.criar_secao_cliente("Cliente 1", 0)
        
        # Cliente 2
        self.criar_secao_cliente("Cliente 2", 1)
        
        # Estados
        self.criar_secao_estados()
        
        # Botões
        self.criar_botoes()
        
        # Status
        self.resultado_label = tk.Label(self.frame_status, text="Pronto para gerar mapa", 
                                       bg=self.config["cor_fundo"], fg="green")
        self.resultado_label.pack()
    
    def criar_secao_cliente(self, nome, indice):
        """Cria seção para entrada de dados do cliente"""
        frame = tk.Frame(self.frame_entrada, bg=self.config["cor_fundo"])
        frame.pack(fill=tk.X, pady=10)
        
        label = tk.Label(frame, text=f"Cidade do {nome}:", 
                        font=("Arial", 12, "bold"),
                        bg=self.config["cor_fundo"])
        label.pack(anchor=tk.W)
        
        combo = ttk.Combobox(frame, width=50, state="readonly")
        combo.pack(fill=tk.X, pady=5)
        
        if indice == 0:
            self.entrada_cliente1 = combo
        else:
            self.entrada_cliente2 = combo
    
    def criar_secao_estados(self):
        """Cria seção para seleção de estados"""
        frame = tk.Frame(self.frame_entrada, bg=self.config["cor_fundo"])
        frame.pack(fill=tk.X, pady=10)
        
        label = tk.Label(frame, text="Estados (selecione vários):", 
                        font=("Arial", 12, "bold"),
                        bg=self.config["cor_fundo"])
        label.pack(anchor=tk.W)
        
        # Frame para listbox e scrollbar
        frame_listbox = tk.Frame(frame, bg=self.config["cor_fundo"])
        frame_listbox.pack(fill=tk.X, pady=5)
        
        self.listbox_estados = tk.Listbox(frame_listbox, selectmode='multiple', height=6)
        scrollbar = tk.Scrollbar(frame_listbox, orient="vertical", command=self.listbox_estados.yview)
        self.listbox_estados.configure(yscrollcommand=scrollbar.set)
        
        self.listbox_estados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def criar_botoes(self):
        """Cria os botões da interface"""
        # Frame para botões em linha
        frame_botoes = tk.Frame(self.frame_botoes, bg=self.config["cor_fundo"])
        frame_botoes.pack()
        
        # Botão Gerar Mapa
        self.botao_gerar = tk.Button(frame_botoes, text="Gerar Mapa", 
                                    command=self.gerar_mapa_com_rotas,
                                    bg=self.config["cor_primaria"], fg="white",
                                    font=("Arial", 12, "bold"),
                                    width=15, height=2)
        self.botao_gerar.pack(side=tk.LEFT, padx=10)
        
        # Botão Abrir Mapa
        self.botao_abrir = tk.Button(frame_botoes, text="Abrir Mapa", 
                                    command=self.abrir_mapa,
                                    bg=self.config["cor_secundaria"], fg="white",
                                    font=("Arial", 12, "bold"),
                                    width=15, height=2)
        self.botao_abrir.pack(side=tk.LEFT, padx=10)
        
        # Botão Carregar Dados
        self.botao_carregar = tk.Button(frame_botoes, text="Carregar Dados", 
                                       command=self.carregar_arquivo,
                                       bg="#28A745", fg="white",
                                       font=("Arial", 12, "bold"),
                                       width=15, height=2)
        self.botao_carregar.pack(side=tk.LEFT, padx=10)
    
    def criar_menu(self):
        """Cria menu da aplicação"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Carregar Dados", command=self.carregar_arquivo)
        menu_arquivo.add_command(label="Sair", command=self.root.quit)
        
        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)
    
    def carregar_dados(self):
        """Carrega os dados do arquivo Excel"""
        try:
            if os.path.exists(self.config["arquivo_dados"]):
                self.df_cidades = pd.read_excel(self.config["arquivo_dados"], sheet_name="Clientes")
                self.df_credenciados = pd.read_excel(self.config["arquivo_dados"], sheet_name="Credenciados")
                
                # Atualizar comboboxes
                cidades = self.df_cidades['nome'].unique().tolist()
                self.entrada_cliente1['values'] = cidades
                self.entrada_cliente2['values'] = cidades
                
                # Atualizar listbox de estados
                self.estados_disponiveis = self.df_credenciados['UF'].unique().tolist()
                self.listbox_estados.delete(0, tk.END)
                for estado in sorted(self.estados_disponiveis):
                    self.listbox_estados.insert(tk.END, estado)
                
                self.atualizar_status(f"Dados carregados: {len(self.df_cidades)} clientes, {len(self.df_credenciados)} credenciados")
            else:
                self.atualizar_status("Arquivo de dados não encontrado. Use 'Carregar Dados' para selecionar um arquivo.")
        except Exception as e:
            self.atualizar_status(f"Erro ao carregar dados: {str(e)}")
    
    def carregar_arquivo(self):
        """Permite ao usuário selecionar arquivo de dados"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo de dados",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if arquivo:
            try:
                self.config["arquivo_dados"] = arquivo
                self.carregar_dados()
                messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")
    
    def calcular_distancia(self, lat1, lon1, lat2, lon2):
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
    
    def gerar_mapa_com_rotas(self):
        """Gera mapa com rotas para credenciados mais próximos"""
        try:
            # Validar dados
            if self.df_cidades is None or self.df_credenciados is None:
                messagebox.showerror("Erro", "Dados não carregados. Carregue um arquivo primeiro.")
                return
            
            cidade_cliente1 = self.entrada_cliente1.get()
            cidade_cliente2 = self.entrada_cliente2.get()
            
            if not cidade_cliente1 or not cidade_cliente2:
                messagebox.showerror("Erro", "Selecione ambas as cidades dos clientes.")
                return
            
            # Buscar coordenadas dos clientes
            cidade1_data = self.df_cidades[self.df_cidades['nome'] == cidade_cliente1]
            cidade2_data = self.df_cidades[self.df_cidades['nome'] == cidade_cliente2]
            
            if cidade1_data.empty or cidade2_data.empty:
                messagebox.showerror("Erro", "Uma ou ambas as cidades não foram encontradas.")
                return
            
            lat1 = float(cidade1_data['LATITUDE'].to_numpy()[0])
            lon1 = float(cidade1_data['LONGITUDE'].to_numpy()[0])
            lat2 = float(cidade2_data['LATITUDE'].to_numpy()[0])
            lon2 = float(cidade2_data['LONGITUDE'].to_numpy()[0])
            
            # Filtrar credenciados por estado
            estados_selecionados = [self.listbox_estados.get(i) for i in self.listbox_estados.curselection()]
            
            if estados_selecionados:
                df_credenciados_filtrados = self.df_credenciados[self.df_credenciados['UF'].isin(estados_selecionados)]
            else:
                df_credenciados_filtrados = self.df_credenciados
            
            if df_credenciados_filtrados.empty:
                messagebox.showwarning("Aviso", "Nenhum credenciado encontrado para os estados selecionados.")
                return
            
            # Encontrar credenciados mais próximos
            df_credenciados_filtrados['distancia1'] = df_credenciados_filtrados.apply(
                lambda row: self.calcular_distancia(lat1, lon1, row['LATITUDE'], row['LONGITUDE']), axis=1
            )
            df_credenciados_filtrados['distancia2'] = df_credenciados_filtrados.apply(
                lambda row: self.calcular_distancia(lat2, lon2, row['LATITUDE'], row['LONGITUDE']), axis=1
            )
            
            cidade_credenciada_mais_proxima1 = df_credenciados_filtrados.loc[df_credenciados_filtrados['distancia1'].idxmin()]
            cidade_credenciada_mais_proxima2 = df_credenciados_filtrados.loc[df_credenciados_filtrados['distancia2'].idxmin()]
            
            # Criar mapa
            mapa = folium.Map(location=[(lat1 + lat2) / 2, (lon1 + lon2) / 2], zoom_start=7)
            
            # Adicionar marcadores dos clientes
            folium.Marker(location=[lat1, lon1], 
                         popup=f"Cliente 1: {cidade_cliente1}", 
                         icon=folium.Icon(color='red', icon='user')).add_to(mapa)
            
            folium.Marker(location=[lat2, lon2], 
                         popup=f"Cliente 2: {cidade_cliente2}", 
                         icon=folium.Icon(color='blue', icon='user')).add_to(mapa)
            
            # Adicionar credenciados mais próximos
            lat_credenciado1 = cidade_credenciada_mais_proxima1['LATITUDE']
            lon_credenciado1 = cidade_credenciada_mais_proxima1['LONGITUDE']
            lat_credenciado2 = cidade_credenciada_mais_proxima2['LATITUDE']
            lon_credenciado2 = cidade_credenciada_mais_proxima2['LONGITUDE']
            
            folium.Marker(location=[lat_credenciado1, lon_credenciado1], 
                         popup=f"Credenciado 1: {cidade_credenciada_mais_proxima1['nome']}<br>Distância: {cidade_credenciada_mais_proxima1['distancia1']:.2f} km", 
                         icon=folium.Icon(color='green', icon='hospital-o')).add_to(mapa)
            
            folium.Marker(location=[lat_credenciado2, lon_credenciado2], 
                         popup=f"Credenciado 2: {cidade_credenciada_mais_proxima2['nome']}<br>Distância: {cidade_credenciada_mais_proxima2['distancia2']:.2f} km", 
                         icon=folium.Icon(color='green', icon='hospital-o')).add_to(mapa)
            
            # Adicionar rotas
            folium.PolyLine(locations=[[lat1, lon1], [lat_credenciado1, lon_credenciado1]], 
                           color='purple', weight=3, opacity=0.8).add_to(mapa)
            folium.PolyLine(locations=[[lat2, lon2], [lat_credenciado2, lon_credenciado2]], 
                           color='purple', weight=3, opacity=0.8).add_to(mapa)
            
            # Adicionar todos os credenciados filtrados
            for _, row in df_credenciados_filtrados.iterrows():
                folium.Marker(location=[row['LATITUDE'], row['LONGITUDE']],
                             popup=f"{row['nome']}<br>UF: {row['UF']}",
                             icon=folium.Icon(color='lightgreen', icon='info-sign')).add_to(mapa)
            
            # Salvar mapa
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"mapa_credenciados_{timestamp}.html"
            mapa.save(nome_arquivo)
            
            self.atualizar_status(f"Mapa gerado com sucesso! Arquivo: {nome_arquivo}")
            messagebox.showinfo("Sucesso", f"Mapa gerado com sucesso!\nArquivo: {nome_arquivo}")
            
        except Exception as e:
            self.atualizar_status(f"Erro ao gerar mapa: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao gerar mapa: {str(e)}")
    
    def abrir_mapa(self):
        """Abre o mapa gerado no navegador"""
        try:
            # Procurar pelo arquivo de mapa mais recente
            arquivos_mapa = [f for f in os.listdir('.') if f.startswith('mapa_credenciados_') and f.endswith('.html')]
            
            if arquivos_mapa:
                arquivo_mais_recente = max(arquivos_mapa, key=os.path.getctime)
                webbrowser.open(arquivo_mais_recente)
                self.atualizar_status(f"Mapa aberto: {arquivo_mais_recente}")
            else:
                messagebox.showwarning("Aviso", "Nenhum mapa encontrado. Gere um mapa primeiro!")
        except Exception as e:
            self.atualizar_status(f"Erro ao abrir mapa: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao abrir mapa: {str(e)}")
    
    def atualizar_status(self, mensagem):
        """Atualiza a mensagem de status"""
        self.resultado_label.config(text=mensagem)
        self.root.update()
    
    def mostrar_sobre(self):
        """Mostra informações sobre o sistema"""
        messagebox.showinfo("Sobre", 
                           "Sistema de Busca de Credenciados\n\n"
                           "Versão: 2.0\n"
                           "Desenvolvido para Engemed\n\n"
                           "Funcionalidades:\n"
                           "- Busca de credenciados por proximidade\n"
                           "- Geração de mapas interativos\n"
                           "- Filtro por estados\n"
                           "- Interface moderna e intuitiva")
    
    def executar(self):
        """Executa a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SistemaCredenciados()
    app.executar() 