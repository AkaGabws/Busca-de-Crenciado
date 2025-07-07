# Sistema de Busca de Credenciados - Versão Web

## 🚀 Nova Versão com Interface Web Moderna

O sistema foi completamente reformulado com uma interface web moderna usando Flask, HTML/CSS/JavaScript e banco de dados SQLite.

## ✨ Principais Melhorias

### 🔄 Mudanças Estruturais
- **Banco de Dados SQLite**: Substituiu as planilhas Excel por um banco de dados robusto
- **Interface Web**: Interface moderna e responsiva no navegador
- **API REST**: Backend com APIs para todas as operações
- **Mapas Integrados**: Visualização direta na aplicação web

### 🎨 Interface Moderna
- **Design Responsivo**: Funciona em desktop, tablet e mobile
- **Bootstrap 5**: Framework CSS moderno
- **Font Awesome**: Ícones profissionais
- **Animações**: Transições suaves e feedback visual
- **Tema Personalizado**: Cores e estilos da Engemed

### 🗄️ Banco de Dados
- **SQLite**: Banco de dados leve e eficiente
- **Tabelas Relacionadas**: Clientes, Credenciados e Histórico
- **Importação Excel**: Mantém compatibilidade com arquivos Excel
- **Dados de Exemplo**: Criação automática de dados para teste

## 📁 Estrutura do Projeto

```
Busca-de-Crenciado/
├── app_web.py              # Aplicação Flask principal
├── database.py             # Gerenciador do banco de dados
├── requirements.txt        # Dependências Python
├── templates/
│   └── index.html         # Template HTML principal
├── static/
│   ├── css/
│   │   └── style.css      # Estilos personalizados
│   ├── js/
│   │   └── app.js         # JavaScript da aplicação
│   └── mapas/             # Mapas gerados
├── credenciados.db        # Banco de dados SQLite
└── README_WEB.md          # Esta documentação
```

## 🛠️ Instalação e Uso

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação
```bash
python app_web.py
```

### 3. Acessar no Navegador
```
http://localhost:5000
```

## 🎯 Funcionalidades

### 📊 Gerenciamento de Dados
- **Criar Dados de Exemplo**: Gera automaticamente dados para teste
- **Importar Excel**: Carrega dados de arquivos Excel existentes
- **Banco Persistente**: Dados salvos automaticamente no SQLite

### 🗺️ Geração de Mapas
- **Seleção de Clientes**: Interface intuitiva para escolher clientes
- **Filtro por Estados**: Seleção múltipla de estados
- **Mapas Interativos**: Visualização direta na aplicação
- **Histórico**: Registro de todos os mapas gerados

### 📱 Interface Responsiva
- **Desktop**: Layout completo com painel lateral
- **Tablet**: Interface adaptada para telas médias
- **Mobile**: Layout otimizado para smartphones

## 🔧 APIs Disponíveis

### GET /api/clientes
Retorna lista de todos os clientes

### GET /api/estados
Retorna lista de estados disponíveis

### GET /api/credenciados?uf=SP
Retorna credenciados, opcionalmente filtrados por UF

### POST /api/gerar-mapa
Gera mapa com dados dos clientes selecionados

### GET /api/historico
Retorna histórico de mapas gerados

### POST /api/importar-excel
Importa dados de arquivo Excel

### GET /api/criar-dados-exemplo
Cria dados de exemplo no banco

## 🎨 Personalização

### Cores e Temas
As cores podem ser personalizadas editando as variáveis CSS em `static/css/style.css`:

```css
:root {
    --primary-color: #2E86AB;    /* Cor principal */
    --secondary-color: #A23B72;  /* Cor secundária */
    --success-color: #28A745;    /* Cor de sucesso */
    --info-color: #17A2B8;       /* Cor de informação */
}
```

### Configurações do Banco
O banco de dados é configurado automaticamente no arquivo `database.py`.

## 📊 Estrutura do Banco de Dados

### Tabela: clientes
```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: credenciados
```sql
CREATE TABLE credenciados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    uf TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: mapas_gerados
```sql
CREATE TABLE mapas_gerados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_arquivo TEXT NOT NULL,
    cliente1_id INTEGER,
    cliente2_id INTEGER,
    estados_filtro TEXT,
    data_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente1_id) REFERENCES clientes (id),
    FOREIGN KEY (cliente2_id) REFERENCES clientes (id)
);
```

## 🚀 Como Usar

### 1. Primeira Execução
1. Execute `python app_web.py`
2. Acesse `http://localhost:5000`
3. Clique em "Criar Dados de Exemplo" para gerar dados de teste

### 2. Gerar Mapa
1. Selecione dois clientes diferentes
2. Opcionalmente, selecione estados para filtrar
3. Clique em "Gerar Mapa"
4. O mapa será exibido diretamente na aplicação

### 3. Importar Dados
1. Clique em "Importar Excel"
2. Selecione arquivo com abas "Clientes" e "Credenciados"
3. Clique em "Importar"

### 4. Visualizar Histórico
- O histórico de mapas gerados aparece no painel lateral
- Clique em "Visualizar" para reabrir um mapa anterior

## 🔍 Recursos Técnicos

### Frontend
- **HTML5**: Estrutura semântica
- **CSS3**: Estilos modernos com variáveis CSS
- **JavaScript ES6+**: Funcionalidades interativas
- **Bootstrap 5**: Framework CSS responsivo
- **Font Awesome**: Ícones profissionais

### Backend
- **Flask**: Framework web Python
- **SQLite**: Banco de dados
- **Pandas**: Manipulação de dados
- **Folium**: Geração de mapas

### Funcionalidades Avançadas
- **Validação em Tempo Real**: Verificação de seleções
- **Loading States**: Feedback visual durante operações
- **Error Handling**: Tratamento robusto de erros
- **Responsive Design**: Adaptação a diferentes telas

## 🎉 Vantagens da Nova Versão

### ✅ Melhorias de Usabilidade
- Interface mais intuitiva e moderna
- Feedback visual em tempo real
- Validação automática de dados
- Histórico de operações

### ✅ Melhorias Técnicas
- Banco de dados estruturado
- APIs RESTful
- Código modular e organizado
- Tratamento robusto de erros

### ✅ Melhorias de Performance
- Carregamento mais rápido
- Menos dependências externas
- Dados persistentes
- Interface responsiva

## 🔧 Solução de Problemas

### Erro de Conexão
- Verifique se a porta 5000 está livre
- Reinicie a aplicação se necessário

### Erro de Banco de Dados
- O banco é criado automaticamente
- Verifique permissões de escrita na pasta

### Erro de Importação
- Verifique se o arquivo Excel tem as abas corretas
- Confirme se as colunas estão nomeadas corretamente

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs no terminal
2. Consulte a documentação
3. Teste com dados de exemplo primeiro

---

**Sistema de Busca de Credenciados v3.0** - Desenvolvido para Engemed 