document.addEventListener('DOMContentLoaded', function () {
  const codigoInput = document.getElementById('codigoStatus');
  const nomeInput = document.getElementById('nomeStatus');
  const btnAdicionar = document.getElementById('btnAdicionar');
  const btnLimpar = document.getElementById('btnLimpar');
  const tabelaBody = document.getElementById('tabelaStatus');

  function limparFormulario() {
    codigoInput.value = '';
    nomeInput.value = '';
  }

  function carregarStatus() {
    fetch('/status/listar')
      .then(response => response.json())
      .then(data => {
        tabelaBody.innerHTML = '';

        if (data.length === 0) {
          const linha = document.createElement('tr');
          linha.innerHTML = `
            <td colspan="3" class="text-center">Nenhum status cadastrado.</td>
          `;
          tabelaBody.appendChild(linha);
          return;
        }

        data.forEach(status => {
          const linha = document.createElement('tr');
          linha.innerHTML = `
            <td>${status.codigo}</td>
            <td>${status.nome}</td>
            <td>
              <button class="btn-icon-only btn-excluir" data-id="${status.id}" title="Excluir">
                <i class="fas fa-trash-alt btn-remover"></i>
              </button>
            </td>
          `;
          tabelaBody.appendChild(linha);
        });

        // Adiciona eventos de exclusão
        document.querySelectorAll('.btn-excluir').forEach(botao => {
          botao.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            if (confirm('Deseja realmente excluir este status?')) {
              fetch('/status/deletar/' + id, {
                method: 'DELETE'
              }).then(() => carregarStatus());
            }
          });
        });
      });
  }

  btnAdicionar.addEventListener('click', function () {
    const codigo = codigoInput.value.trim();
    const nome = nomeInput.value.trim();

    if (!codigo || !nome) {
      alert('Preencha todos os campos.');
      return;
    }

    fetch('/status/adicionar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ codigo, nome })
    })
      .then(response => response.json())
      .then(() => {
        limparFormulario();
        carregarStatus();
      });
  });

  btnLimpar.addEventListener('click', limparFormulario);

  carregarStatus();
});