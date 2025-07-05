function abrirAbaPerfil() {
    document.getElementById('abaPerfil').classList.add('active');
    document.getElementById('abaSeguranca').classList.remove('active');
    document.querySelectorAll('.tab-button')[0].classList.add('active');
    document.querySelectorAll('.tab-button')[1].classList.remove('active');
}

function abrirAbaSeguranca() {
    document.getElementById('abaPerfil').classList.remove('active');
    document.getElementById('abaSeguranca').classList.add('active');
    document.querySelectorAll('.tab-button')[0].classList.remove('active');
    document.querySelectorAll('.tab-button')[1].classList.add('active');
}

function adicionarGrupoAcesso() {
    const container = document.getElementById('gruposAcessoContainer');
    const novoGrupo = document.createElement('div');
    novoGrupo.className = 'perfil-grupo-acesso-item';

    novoGrupo.innerHTML = `
        <input type="radio" name="grupoAcessoSelecionado" />

        <!-- Campo visível com autocomplete -->
        <input type="text"
               name="projetosSelecionadosNomes[]"
               placeholder="Nome do Projeto"
               class="input-projeto"
               list="projetosDisponiveis"
               oninput="atualizarProjetoSelecionado(this)" />

        <!-- Campo oculto com o ID do projeto -->
        <input type="hidden" name="projetosSelecionados[]" value="" />

        <i class="fas fa-info-circle icon-detalhes"
           onclick="abrirModalDetalhesProjeto(this)"
           data-modal-target="modalProjeto"></i>

        <button type="button" class="btn-remover" onclick="removerGrupoAcesso(this)">
            <i class="fas fa-trash-alt"></i>
        </button>
    `;

    container.appendChild(novoGrupo);
}

function removerGrupoAcesso(botao) {
    const container = document.getElementById('gruposAcessoContainer');
    const item = botao.parentElement;
    const itens = container.querySelectorAll('.perfil-grupo-acesso-item');
    const radioSelecionado = container.querySelector('input[type="radio"]:checked');

    // Impede remover se for o último item
    if (itens.length <= 1) {
        alert("Você não pode remover o último grupo de acesso.");
        return;
    }

    // Impede remover o item que está selecionado
    if (item.contains(radioSelecionado)) {
        alert("Você não pode remover o grupo de acesso selecionado.");
        return;
    }

    item.remove();
}

function atualizarProjetoSelecionado(input) {
    const datalist = document.getElementById('projetosDisponiveis');
    const hiddenInput = input.parentElement.querySelector('input[type="hidden"]');
    const valorDigitado = input.value;

    const optionSelecionada = Array.from(datalist.options).find(opt => opt.value === valorDigitado);
    if (optionSelecionada) {
        hiddenInput.value = optionSelecionada.dataset.id;
    } else {
        hiddenInput.value = ''; // Limpa se não for um projeto válido
    }
}
