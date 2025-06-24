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
    novoGrupo.className = 'grupo-acesso-item';
    novoGrupo.innerHTML = `
        <input type="radio" name="grupoAcessoSelecionado">
        <input type="text" name="grupoAcesso[]" placeholder="Grupo de Acesso">
        <button type="button" class="btn-remover" onclick="removerGrupoAcesso(this)">
            <i class="fas fa-trash-alt"></i>
        </button>
    `;
    container.appendChild(novoGrupo);
}

function removerGrupoAcesso(botao) {
    const item = botao.parentElement;
    item.remove();
}
