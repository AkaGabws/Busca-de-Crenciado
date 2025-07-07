# Instruções de Uso - Sistema de Busca de Credenciados

## 🚀 Como Usar o Sistema

### 1. Primeira Execução
1. Execute o arquivo `app.py`:
   ```bash
   python app.py
   ```

2. O sistema irá carregar automaticamente os dados de exemplo

### 2. Interface Principal

A interface possui as seguintes seções:

#### 📍 Seleção de Clientes
- **Cliente 1**: Selecione a primeira cidade do cliente
- **Cliente 2**: Selecione a segunda cidade do cliente

#### 🗺️ Filtro de Estados
- Selecione um ou mais estados para filtrar os credenciados
- Use Ctrl+Click para selecionar múltiplos estados
- Deixe vazio para incluir todos os estados

#### 🔘 Botões Principais
- **Gerar Mapa**: Cria um mapa interativo com as rotas
- **Abrir Mapa**: Abre o mapa gerado no navegador
- **Carregar Dados**: Permite selecionar um arquivo Excel diferente

### 3. Como Gerar um Mapa

1. **Selecione as cidades dos clientes**:
   - Escolha duas cidades diferentes das listas suspensas

2. **Filtre por estados** (opcional):
   - Selecione os estados onde deseja buscar credenciados
   - Se não selecionar nenhum, todos os estados serão incluídos

3. **Clique em "Gerar Mapa"**:
   - O sistema calculará as distâncias
   - Encontrará os credenciados mais próximos
   - Gerará um arquivo HTML com o mapa

4. **Visualize o resultado**:
   - Clique em "Abrir Mapa" para ver no navegador
   - Ou procure pelo arquivo `mapa_credenciados_YYYYMMDD_HHMMSS.html`

### 4. Interpretando o Mapa

#### 🎯 Marcadores no Mapa:
- **🔴 Vermelho**: Cliente 1
- **🔵 Azul**: Cliente 2
- **🟢 Verde**: Credenciados mais próximos (com rotas)
- **🟡 Verde claro**: Outros credenciados disponíveis

#### 📏 Informações Exibidas:
- **Distâncias**: Calculadas em quilômetros
- **Rotas**: Linhas roxas conectando clientes aos credenciados
- **Popups**: Informações detalhadas ao clicar nos marcadores

### 5. Usando Seus Próprios Dados

#### 📊 Estrutura do Arquivo Excel:
O arquivo deve ter duas abas:

**Aba "Clientes":**
| nome | LATITUDE | LONGITUDE |
|------|----------|-----------|
| São Paulo | -23.5505 | -46.6333 |

**Aba "Credenciados":**
| nome | UF | LATITUDE | LONGITUDE |
|------|----|----------|-----------|
| Hospital ABC | SP | -23.5505 | -46.6333 |

#### 🔄 Como Carregar:
1. Clique em "Carregar Dados"
2. Selecione seu arquivo Excel
3. O sistema atualizará automaticamente as listas

### 6. Dicas de Uso

#### 💡 Para Melhores Resultados:
- Use coordenadas precisas (latitude/longitude)
- Verifique se os nomes das cidades estão corretos
- Selecione estados específicos para resultados mais relevantes

#### 🔧 Solução de Problemas:
- **"Cidade não encontrada"**: Verifique se o nome está correto no arquivo
- **"Nenhum credenciado encontrado"**: Tente selecionar mais estados
- **Erro ao gerar mapa**: Verifique se as coordenadas são válidas

### 7. Funcionalidades Avançadas

#### 📋 Menu Arquivo:
- **Carregar Dados**: Selecionar arquivo Excel
- **Sair**: Fechar aplicação

#### ❓ Menu Ajuda:
- **Sobre**: Informações do sistema

### 8. Arquivos Gerados

O sistema cria automaticamente:
- `dados_credenciados.xlsx`: Dados de exemplo
- `config.json`: Configurações do sistema
- `mapa_credenciados_*.html`: Mapas gerados

---

## 🎯 Exemplo Prático

1. **Execute**: `python app.py`
2. **Selecione**: "São Paulo" como Cliente 1
3. **Selecione**: "Rio de Janeiro" como Cliente 2
4. **Filtre**: Selecione "SP" e "RJ" nos estados
5. **Gere**: Clique em "Gerar Mapa"
6. **Visualize**: Clique em "Abrir Mapa"

Resultado: Um mapa mostrando os credenciados mais próximos de cada cliente com as rotas calculadas! 