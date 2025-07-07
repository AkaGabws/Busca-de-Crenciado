# Sistema de Busca de Credenciados

Sistema para localizar credenciados próximos a clientes usando mapas interativos.

## Funcionalidades

- Busca de credenciados por proximidade geográfica
- Geração de mapas interativos com rotas
- Filtro por estados
- Interface gráfica intuitiva
- Cálculo de distâncias em tempo real

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Prepare os dados:
   - Crie um arquivo Excel com duas abas: "Clientes" e "Credenciados"
   - A aba "Clientes" deve ter colunas: nome, LATITUDE, LONGITUDE
   - A aba "Credenciados" deve ter colunas: nome, UF, LATITUDE, LONGITUDE

3. Execute o programa:
```bash
python app.py
```

## Estrutura dos Dados

### Aba "Clientes"
| nome | LATITUDE | LONGITUDE |
|------|----------|-----------|
| São Paulo | -23.5505 | -46.6333 |

### Aba "Credenciados"
| nome | UF | LATITUDE | LONGITUDE |
|------|----|----------|-----------|
| Hospital ABC | SP | -23.5505 | -46.6333 |

## Como Usar

1. Selecione duas cidades de clientes
2. Escolha os estados para filtrar credenciados
3. Clique em "Gerar Mapa"
4. Use "Abrir Mapa" para visualizar o resultado 