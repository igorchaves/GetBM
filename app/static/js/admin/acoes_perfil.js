function abrirAbaPerfil() {
    document.getElementById('abaPerfil').classList.add('active');
    document.getElementById('abaSeguranca').classList.remove('active');

    const botoes = document.querySelectorAll('.perfil-tab-button');
    botoes[0].classList.add('active');
    botoes[1].classList.remove('active');
}

function abrirAbaSeguranca() {
    document.getElementById('abaPerfil').classList.remove('active');
    document.getElementById('abaSeguranca').classList.add('active');

    const botoes = document.querySelectorAll('.perfil-tab-button');
    botoes[0].classList.remove('active');
    botoes[1].classList.add('active');
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

    if (itens.length <= 1) {
        alert("Você não pode remover o último grupo de acesso.");
        return;
    }

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
    hiddenInput.value = optionSelecionada ? optionSelecionada.dataset.id : '';
}

document.getElementById('formPerfilUsuario').addEventListener('submit', function (e) {
    const novaSenha = document.getElementById('novaSenha').value;
    const confirmarSenha = document.getElementById('confirmarSenha').value;

    if (novaSenha || confirmarSenha) {
        if (novaSenha === confirmarSenha) {
            alert('Senha será atualizada ao salvar o formulário.');
        } else {
            alert('As senhas não coincidem. A senha não será atualizada.');
        }
    }
});
