// Sistema de Busca de Credenciados - JavaScript

class SistemaCredenciados {
    constructor() {
        this.clientes = [];
        this.estados = [];
        this.estadosSelecionados = [];
        this.init();
    }

    async init() {
        await this.carregarDados();
        this.setupEventListeners();
        this.atualizarStatus('Sistema carregado com sucesso!', 'success');
    }

    async carregarDados() {
        try {
            // Carregar clientes
            const responseClientes = await fetch('/api/clientes');
            const dataClientes = await responseClientes.json();
            if (dataClientes.success) {
                this.clientes = dataClientes.data;
                this.preencherSelectClientes();
            }

            // Carregar estados
            const responseEstados = await fetch('/api/estados');
            const dataEstados = await responseEstados.json();
            if (dataEstados.success) {
                this.estados = dataEstados.data;
                this.preencherEstados();
            }

            // Carregar histórico
            await this.carregarHistorico();

        } catch (error) {
            console.error('Erro ao carregar dados:', error);
            this.atualizarStatus('Erro ao carregar dados', 'danger');
        }
    }

    preencherSelectClientes() {
        const selectCliente1 = document.getElementById('cliente1');
        const selectCliente2 = document.getElementById('cliente2');

        // Limpar opções existentes
        selectCliente1.innerHTML = '<option value="">Selecione o cliente 1...</option>';
        selectCliente2.innerHTML = '<option value="">Selecione o cliente 2...</option>';

        // Adicionar clientes
        this.clientes.forEach(cliente => {
            const option1 = document.createElement('option');
            option1.value = cliente.id;
            option1.textContent = cliente.nome;
            selectCliente1.appendChild(option1);

            const option2 = document.createElement('option');
            option2.value = cliente.id;
            option2.textContent = cliente.nome;
            selectCliente2.appendChild(option2);
        });
    }

    preencherEstados() {
        const container = document.getElementById('estados-container');
        container.innerHTML = '';

        this.estados.forEach(estado => {
            const div = document.createElement('div');
            div.className = 'estado-item';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'form-check-input me-2';
            checkbox.id = `estado-${estado}`;
            checkbox.value = estado;
            
            const label = document.createElement('label');
            label.className = 'form-check-label';
            label.htmlFor = `estado-${estado}`;
            label.textContent = estado;
            
            div.appendChild(checkbox);
            div.appendChild(label);
            container.appendChild(div);

            // Event listener para checkbox
            checkbox.addEventListener('change', (e) => {
                if (e.target.checked) {
                    this.estadosSelecionados.push(estado);
                } else {
                    this.estadosSelecionados = this.estadosSelecionados.filter(e => e !== estado);
                }
            });
        });
    }

    async carregarHistorico() {
        try {
            const response = await fetch('/api/historico');
            const data = await response.json();
            
            if (data.success) {
                this.exibirHistorico(data.data);
            }
        } catch (error) {
            console.error('Erro ao carregar histórico:', error);
        }
    }

    exibirHistorico(historico) {
        const container = document.getElementById('historico-container');
        
        if (historico.length === 0) {
            container.innerHTML = '<p class="text-muted">Nenhum mapa gerado ainda</p>';
            return;
        }

        container.innerHTML = '';
        historico.slice(0, 5).forEach(item => {
            const div = document.createElement('div');
            div.className = 'historico-item fade-in';
            
            const data = new Date(item.data_geracao).toLocaleString('pt-BR');
            const estados = item.estados_filtro ? item.estados_filtro.split(',').join(', ') : 'Todos';
            
            div.innerHTML = `
                <h6>${item.cliente1_nome} → ${item.cliente2_nome}</h6>
                <p><small>Estados: ${estados}</small></p>
                <p><small>Data: ${data}</small></p>
                <button class="btn btn-sm btn-outline-primary" onclick="sistema.visualizarMapa('${item.nome_arquivo}')">
                    <i class="fas fa-eye me-1"></i>Visualizar
                </button>
            `;
            
            container.appendChild(div);
        });
    }

    async gerarMapa() {
        const cliente1Id = document.getElementById('cliente1').value;
        const cliente2Id = document.getElementById('cliente2').value;

        if (!cliente1Id || !cliente2Id) {
            this.atualizarStatus('Selecione ambos os clientes', 'warning');
            return;
        }

        if (cliente1Id === cliente2Id) {
            this.atualizarStatus('Selecione clientes diferentes', 'warning');
            return;
        }

        this.atualizarStatus('Gerando mapa...', 'info');
        this.mostrarLoading(true);

        try {
            const response = await fetch('/api/gerar-mapa', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    cliente1_id: parseInt(cliente1Id),
                    cliente2_id: parseInt(cliente2Id),
                    estados_filtro: this.estadosSelecionados
                })
            });

            const data = await response.json();

            if (data.success) {
                this.atualizarStatus('Mapa gerado com sucesso!', 'success');
                await this.visualizarMapa(data.arquivo);
                await this.carregarHistorico();
                
                // Mostrar distâncias
                const distancias = data.distancias;
                this.mostrarDistancias(distancias);
            } else {
                this.atualizarStatus(`Erro: ${data.error}`, 'danger');
            }

        } catch (error) {
            console.error('Erro ao gerar mapa:', error);
            this.atualizarStatus('Erro ao gerar mapa', 'danger');
        } finally {
            this.mostrarLoading(false);
        }
    }

    async visualizarMapa(nomeArquivo) {
        const container = document.getElementById('mapa-container');
        
        try {
            // Criar iframe para exibir o mapa
            container.innerHTML = `
                <iframe 
                    src="/mapa/${nomeArquivo}" 
                    width="100%" 
                    height="100%" 
                    frameborder="0"
                    style="border-radius: 8px;"
                ></iframe>
            `;
        } catch (error) {
            console.error('Erro ao visualizar mapa:', error);
            this.atualizarStatus('Erro ao carregar mapa', 'danger');
        }
    }

    mostrarDistancias(distancias) {
        const mensagem = `
            Distâncias calculadas:<br>
            Cliente 1 → Credenciado: ${distancias.cliente1_credenciado1} km<br>
            Cliente 2 → Credenciado: ${distancias.cliente2_credenciado2} km
        `;
        
        this.atualizarStatus(mensagem, 'success');
    }

    async criarDadosExemplo() {
        this.atualizarStatus('Criando dados de exemplo...', 'info');
        this.mostrarLoading(true);

        try {
            const response = await fetch('/api/criar-dados-exemplo');
            const data = await response.json();

            if (data.success) {
                this.atualizarStatus(data.message, 'success');
                await this.carregarDados();
            } else {
                this.atualizarStatus(`Erro: ${data.error}`, 'danger');
            }

        } catch (error) {
            console.error('Erro ao criar dados de exemplo:', error);
            this.atualizarStatus('Erro ao criar dados de exemplo', 'danger');
        } finally {
            this.mostrarLoading(false);
        }
    }

    async importarExcel() {
        const fileInput = document.getElementById('arquivoExcel');
        const file = fileInput.files[0];

        if (!file) {
            this.atualizarStatus('Selecione um arquivo Excel', 'warning');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        this.atualizarStatus('Importando dados...', 'info');
        this.mostrarLoading(true);

        try {
            const response = await fetch('/api/importar-excel', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.atualizarStatus(data.message, 'success');
                await this.carregarDados();
                
                // Fechar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('importarModal'));
                modal.hide();
                
                // Limpar input
                fileInput.value = '';
            } else {
                this.atualizarStatus(`Erro: ${data.error}`, 'danger');
            }

        } catch (error) {
            console.error('Erro ao importar Excel:', error);
            this.atualizarStatus('Erro ao importar arquivo', 'danger');
        } finally {
            this.mostrarLoading(false);
        }
    }

    setupEventListeners() {
        // Botão gerar mapa
        document.getElementById('gerarMapa').addEventListener('click', () => {
            this.gerarMapa();
        });

        // Botão criar dados de exemplo
        document.getElementById('criarDadosExemplo').addEventListener('click', () => {
            this.criarDadosExemplo();
        });

        // Botão importar Excel
        document.getElementById('importarBtn').addEventListener('click', () => {
            this.importarExcel();
        });

        // Validação de seleção de clientes
        document.getElementById('cliente1').addEventListener('change', () => {
            this.validarSelecaoClientes();
        });

        document.getElementById('cliente2').addEventListener('change', () => {
            this.validarSelecaoClientes();
        });
    }

    validarSelecaoClientes() {
        const cliente1 = document.getElementById('cliente1').value;
        const cliente2 = document.getElementById('cliente2').value;
        const btnGerar = document.getElementById('gerarMapa');

        if (cliente1 && cliente2 && cliente1 !== cliente2) {
            btnGerar.disabled = false;
            btnGerar.classList.remove('btn-secondary');
            btnGerar.classList.add('btn-primary');
        } else {
            btnGerar.disabled = true;
            btnGerar.classList.remove('btn-primary');
            btnGerar.classList.add('btn-secondary');
        }
    }

    atualizarStatus(mensagem, tipo = 'info') {
        const statusDiv = document.getElementById('status');
        const statusText = document.getElementById('status-text');

        statusText.innerHTML = mensagem;
        statusDiv.className = `alert alert-${tipo}`;
        statusDiv.classList.remove('d-none');

        // Auto-hide após 5 segundos para mensagens de sucesso
        if (tipo === 'success') {
            setTimeout(() => {
                statusDiv.classList.add('d-none');
            }, 5000);
        }
    }

    mostrarLoading(mostrar) {
        const btnGerar = document.getElementById('gerarMapa');
        const btnCriar = document.getElementById('criarDadosExemplo');
        const btnImportar = document.getElementById('importarBtn');

        if (mostrar) {
            btnGerar.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Gerando...';
            btnCriar.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Criando...';
            btnImportar.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Importando...';
            
            btnGerar.disabled = true;
            btnCriar.disabled = true;
            btnImportar.disabled = true;
        } else {
            btnGerar.innerHTML = '<i class="fas fa-map me-1"></i>Gerar Mapa';
            btnCriar.innerHTML = '<i class="fas fa-database me-1"></i>Criar Dados de Exemplo';
            btnImportar.innerHTML = '<i class="fas fa-upload me-1"></i>Importar';
            
            btnGerar.disabled = false;
            btnCriar.disabled = false;
            btnImportar.disabled = false;
        }
    }

    // Método para limpar seleções
    limparSelecoes() {
        document.getElementById('cliente1').value = '';
        document.getElementById('cliente2').value = '';
        
        // Limpar checkboxes de estados
        this.estadosSelecionados = [];
        document.querySelectorAll('#estados-container input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });

        this.validarSelecaoClientes();
        this.atualizarStatus('Seleções limpas', 'info');
    }
}

// Inicializar sistema quando a página carregar
let sistema;
document.addEventListener('DOMContentLoaded', () => {
    sistema = new SistemaCredenciados();
});

// Função global para visualizar mapa (usada no histórico)
function visualizarMapa(nomeArquivo) {
    if (sistema) {
        sistema.visualizarMapa(nomeArquivo);
    }
} 