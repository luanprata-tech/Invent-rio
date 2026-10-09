let isSaving = false;

function disableAllButtons() {
    document.querySelectorAll('button').forEach(btn => {
        btn.disabled = true;
        btn.classList.add('opacity-50', 'cursor-not-allowed');
    });
}



function resetSavingState() {
    isSaving = false;
    document.querySelectorAll('button').forEach(btn => {
        if (btn.disabled && btn.classList.contains('opacity-50')) {
            btn.disabled = false;
            btn.classList.remove('opacity-50', 'cursor-not-allowed');
        }
    });
}


function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    const toast = document.createElement('div');
    const bgColor = type === 'success' ? 'bg-primary' : 'bg-error';
    const icon = type === 'success' ? 'check_circle' : 'error';
    
    toast.className = `flex items-center gap-2 px-4 py-3 rounded-lg shadow-lg text-white font-label-md transition-all duration-300 transform translate-y-10 opacity-0 ${bgColor}`;
    toast.innerHTML = `<span class="material-symbols-outlined text-[20px]">${icon}</span> <span>${message}</span>`;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.remove('translate-y-10', 'opacity-0');
    }, 10);
    
    setTimeout(() => {
        toast.classList.add('translate-y-10', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}


  function limparFiltros() {
    document.getElementById('filtro-texto').value = '';
    document.getElementById('filtro-setor').value = '';
    document.getElementById('filtro-fonte').value = '';
    document.getElementById('filtro-situacao').value = '';
    const btnTodos = document.querySelector('.card-filtro-cat[data-cat="todos"]');
    if (btnTodos) filtrarPorCategoria('todos', btnTodos);
  }




// Modal Atributos
function abrirModalAtributos() {
    const modal = document.getElementById('modal-atributos');
    modal.classList.remove('hidden');
    // small delay to allow display:block to apply before opacity transition
    setTimeout(() => {
        modal.classList.remove('opacity-0', 'pointer-events-none');
    }, 10);
}

function fecharModalAtributos() {
    const modal = document.getElementById('modal-atributos');
    modal.classList.add('opacity-0', 'pointer-events-none');
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 300); // Wait for transition
}

function switchTab(tabName, btn) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    // Remove active styles from all buttons
    document.querySelectorAll('.tab-btn').forEach(el => {
        el.classList.remove('border-primary', 'text-primary');
        el.classList.add('border-transparent', 'text-on-surface-variant');
    });
    
    // Show selected tab
    document.getElementById('tab-' + tabName).classList.remove('hidden');
    // Add active styles to clicked button
    btn.classList.remove('border-transparent', 'text-on-surface-variant');
    btn.classList.add('border-primary', 'text-primary');
}

async function salvarAtributo(endpoint, inputId, btn) {
    if (isSaving) return;
    isSaving = true;
    if (btn) { btn.disabled = true; btn.classList.add('opacity-50', 'cursor-not-allowed'); }
    const input = document.getElementById(inputId);
    const name = input.value.trim();
    if (!name) { resetSavingState(); return showToast('Por favor, insira um nome.', 'error'); }

    try {
        const res = await fetch(`/api/attributes/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name })
        });
        
        if (res.ok) {
            showToast('Cadastro salvo com sucesso!', 'success');
            input.value = '';
            disableAllButtons();
            setTimeout(() => window.location.reload(), 1500);
        } else {
            resetSavingState();
            showToast('Erro ao cadastrar.', 'error');
        }
    } catch (e) {
        resetSavingState();
            showToast('Erro ao conectar com o servidor.', 'error');
    }
}


// Cadastrar Novo Equipamento - Form Submit
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-cadastro-equipamento');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (isSaving) return;
            isSaving = true;
            
            const submitBtn = document.querySelector('button[form="form-cadastro-equipamento"][type="submit"]');
            if (submitBtn) { submitBtn.disabled = true; submitBtn.classList.add('opacity-50', 'cursor-not-allowed'); }

            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            // if checkbox was checked, PAT is SEM-PAT (done by UI or we enforce it)
            if (document.getElementById('check-pat-pendente').checked) {
                data.patrimony_number = 'SEM-PAT';
            }

            try {
                const res = await fetch('/api/assets/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                if (res.ok) {
                    showToast('Equipamento cadastrado com sucesso!', 'success');
                    disableAllButtons();
            setTimeout(() => window.location.reload(), 1500);
                } else {
                    const err = await res.json();
                    resetSavingState();
            showToast('Erro ao cadastrar: ' + (err.detail || 'Erro desconhecido'), 'error');
                }
            } catch (error) {
                resetSavingState();
            showToast('Erro ao conectar com o servidor.', 'error');
            }
        });
    }
});



function excluirAtributo(endpoint, id) {
    document.getElementById('delete-attr-endpoint').value = endpoint;
    document.getElementById('delete-attr-id').value = id;
    
    const modal = document.getElementById('modal-delete-atributo');
    modal.classList.remove('hidden');
    setTimeout(() => modal.classList.remove('opacity-0', 'pointer-events-none'), 10);
}

function fecharModalDeleteAtributo() {
    const modal = document.getElementById('modal-delete-atributo');
    modal.classList.add('opacity-0', 'pointer-events-none');
    setTimeout(() => modal.classList.add('hidden'), 300);
}


async function confirmarExclusaoAtributo() {
    if (isSaving) return;
    isSaving = true;
    const endpoint = document.getElementById('delete-attr-endpoint').value;
    const id = document.getElementById('delete-attr-id').value;
    
    try {
        const url = endpoint === 'assets' ? `/api/assets/${id}` : `/api/attributes/${endpoint}/${id}`;
        
        const res = await fetch(url, {
            method: 'DELETE'
        });
        if (res.ok) {
            fecharModalDeleteAtributo();
            showToast('Item excluído com sucesso!', 'success');
            disableAllButtons();
            setTimeout(() => window.location.reload(), 1500);
        } else {
            fecharModalDeleteAtributo();
            resetSavingState();
            showToast('Erro ao excluir item.', 'error');
        }
    } catch (e) {
        fecharModalDeleteAtributo();
        resetSavingState();
            showToast('Erro de conexão.', 'error');
    }
}


function editarAtributo(endpoint, id, oldName) {
    document.getElementById('edit-attr-endpoint').value = endpoint;
    document.getElementById('edit-attr-id').value = id;
    document.getElementById('edit-attr-name').value = oldName;
    
    const modal = document.getElementById('modal-edit-atributo');
    modal.classList.remove('hidden');
    setTimeout(() => modal.classList.remove('opacity-0', 'pointer-events-none'), 10);
}

function fecharModalEditAtributo() {
    const modal = document.getElementById('modal-edit-atributo');
    modal.classList.add('opacity-0', 'pointer-events-none');
    setTimeout(() => modal.classList.add('hidden'), 300);
}

async function salvarEdicaoAtributo(btn) {
    if (isSaving) return;
    isSaving = true;
    if (btn) { btn.disabled = true; btn.classList.add('opacity-50', 'cursor-not-allowed'); }
    const endpoint = document.getElementById('edit-attr-endpoint').value;
    const id = document.getElementById('edit-attr-id').value;
    const newName = document.getElementById('edit-attr-name').value.trim();
    
    if (!newName) {
        resetSavingState();
        showToast('O nome não pode ficar vazio', 'error');
        return;
    }
    
    try {
        const res = await fetch(`/api/attributes/${endpoint}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: newName })
        });
        if (res.ok) {
            fecharModalEditAtributo();
            showToast('Item atualizado com sucesso!', 'success');
            disableAllButtons();
            setTimeout(() => window.location.reload(), 1500);
        } else {
            resetSavingState();
            showToast('Erro ao atualizar item.', 'error');
        }
    } catch (e) {
        resetSavingState();
            showToast('Erro de conexão.', 'error');
    }
}


// FUNCOES PARA EDICAO E EXCLUSAO DE EQUIPAMENTO

async function abrirDetalhesEquipamento(id) {
    try {
        const res = await fetch(`/api/assets/${id}`);
        if (!res.ok) {
            resetSavingState();
            showToast('Erro ao carregar detalhes do equipamento.', 'error');
            return;
        }
        const data = await res.json();
        
        // Populate the form
        document.getElementById('edit-equipamento-id').value = data.id;
        const form = document.getElementById('form-edit-equipamento');
        
        // Populate selects and inputs by name
        for (const [key, value] of Object.entries(data)) {
            const input = form.elements[key];
            if (input) {
                input.value = value;
            }
        }
        
        // Special logic for patrimony
        const patInput = document.getElementById('edit-input-novo-pat');
        const patCheck = document.getElementById('edit-check-pat-pendente');
        if (data.patrimony_number === 'SEM-PAT') {
            patCheck.checked = true;
            patInput.value = '';
            patInput.disabled = true;
            patInput.classList.add('opacity-60', 'cursor-not-allowed');
        } else {
            patCheck.checked = false;
            patInput.value = data.patrimony_number;
            patInput.disabled = false;
            patInput.classList.remove('opacity-60', 'cursor-not-allowed');
        }
        
        // IP special case (since it's a list in API, we show the first one if any)
        if (data.ips && data.ips.length > 0) {
            form.elements['ip_address'].value = data.ips[0];
        } else {
            form.elements['ip_address'].value = '';
        }

        const modal = document.getElementById('modal-edit-equipamento');
        modal.classList.remove('hidden');
        setTimeout(() => modal.classList.remove('opacity-0', 'pointer-events-none'), 10);
    } catch (e) {
        resetSavingState();
            showToast('Erro de conexão.', 'error');
    }
}

function fecharModalEditEquipamento() {
    const modal = document.getElementById('modal-edit-equipamento');
    modal.classList.add('opacity-0', 'pointer-events-none');
    setTimeout(() => modal.classList.add('hidden'), 300);
}

function toggleEditPatPendente(checkbox) {
    const input = document.getElementById('edit-input-novo-pat');
    if (checkbox.checked) {
        input.disabled = true;
        input.value = '';
        input.classList.add('opacity-60', 'cursor-not-allowed');
    } else {
        input.disabled = false;
        input.classList.remove('opacity-60', 'cursor-not-allowed');
    }
}

async function salvarEdicaoEquipamento(btn) {
    if (isSaving) return;
    isSaving = true;
    if (btn) { btn.disabled = true; btn.classList.add('opacity-50', 'cursor-not-allowed'); }
    const id = document.getElementById('edit-equipamento-id').value;
    const form = document.getElementById('form-edit-equipamento');
    
    // Check HTML5 validity
    if (!form.checkValidity()) {
        form.reportValidity();
        resetSavingState();
        return;
    }
    
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    if (document.getElementById('edit-check-pat-pendente').checked) {
        data.patrimony_number = 'SEM-PAT';
    }

    try {
        const res = await fetch(`/api/assets/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (res.ok) {
            fecharModalEditEquipamento();
            showToast('Equipamento atualizado com sucesso!', 'success');
            disableAllButtons();
            setTimeout(() => window.location.reload(), 1500);
        } else {
            const err = await res.json();
            resetSavingState();
            showToast('Erro ao atualizar: ' + (err.detail || 'Erro desconhecido'), 'error');
        }
    } catch (error) {
        resetSavingState();
            showToast('Erro ao conectar com o servidor.', 'error');
    }
}


async function confirmarExclusaoEquipamento() {
    const id = document.getElementById('edit-equipamento-id').value;

    
    // Using our custom delete confirmation modal? No wait, we need a separate modal or just a different confirmation. 
    // The user said: "O olho do botao de acoes deve abrir um modal para ediçao e exclusao, lembranco, todas as confirmaçoes... deve aparecer no sistema"
    // I can reuse modal-delete-atributo or create a new one. I'll just reuse modal-delete-atributo!
    document.getElementById('delete-attr-endpoint').value = 'assets';
    document.getElementById('delete-attr-id').value = id;
    
    // Hide edit modal
    fecharModalEditEquipamento();
    
    // Show delete confirmation modal
    const modalDelete = document.getElementById('modal-delete-atributo');
    modalDelete.classList.remove('hidden');
    setTimeout(() => modalDelete.classList.remove('opacity-0', 'pointer-events-none'), 10);
}

function filterModels(brandSelect, modelSelect) {
    const selectedBrand = brandSelect.value;
    const options = modelSelect.querySelectorAll('option');
    options.forEach(opt => {
        if (!opt.value) return; // Keep the default "Selecione..."
        if (opt.getAttribute('data-brand') === selectedBrand || !selectedBrand) {
            opt.style.display = 'block';
        } else {
            opt.style.display = 'none';
        }
    });
    // Reset model value if the selected one is now hidden
    const selectedOpt = modelSelect.querySelector('option:checked');
    if (selectedOpt && selectedOpt.style.display === 'none') {
        modelSelect.value = '';
    }
}

async function salvarModelo(btn) {
    if (isSaving) return;
    isSaving = true;
    if (btn) { btn.disabled = true; btn.classList.add('opacity-50', 'cursor-not-allowed'); }
    const input = document.getElementById('input-modelo');
    const brandSelect = document.getElementById('select-brand-for-model');
    const name = input.value.trim();
    const brand_id = brandSelect ? parseInt(brandSelect.value) : null;
    
    if (!name || isNaN(brand_id)) { 
        resetSavingState(); 
        return showToast('Por favor, selecione a marca e insira um modelo.', 'error'); 
    }

    try {
        const res = await fetch(`/api/attributes/models`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, brand_id })
        });
        
        if (res.ok) {
            showToast('Modelo salvo com sucesso!', 'success');
            input.value = '';
            disableAllButtons();
            setTimeout(() => window.location.reload(), 1500);
        } else {
            resetSavingState();
            showToast('Erro ao cadastrar.', 'error');
        }
    } catch (e) {
        resetSavingState();
        showToast('Erro ao conectar com o servidor.', 'error');
    }
}
