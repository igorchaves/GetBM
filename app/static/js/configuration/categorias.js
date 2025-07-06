document.addEventListener('DOMContentLoaded', function () {
    const codigoInput = document.getElementById('codigo');
    const nomeInput = document.getElementById('nome');
    const btnAdicionar = document.getElementById('btnAdicionar');
    const btnLimpar = document.getElementById('btnLimpar');
    const tabelaCategorias = document.getElementById('tabelaCategorias').getElementsByTagName('tbody')[0];

    function carregarCategorias() {
        fetch('/api/categorias')
            .then(response => response.json())
            .then(data => {
                tabelaCategorias.innerHTML = '';

                if (data.length === 0) {
                    const row = tabelaCategorias.insertRow();
                    const cell = row.insertCell(0);
                    cell.colSpan = 3;
                    cell.style.textAlign = 'center';
                    cell.textContent = 'Nenhuma categoria cadastrada.';
                    return;
                }

                data.forEach(categoria => {
                    const row = tabelaCategorias.insertRow();
                    row.innerHTML = `
                        <td>${categoria.codigo}</td>
                        <td>${categoria.nome}</td>
                        <td>
                            <form onsubmit="return excluirCategoria(${categoria.id})" style="display:inline;">
                                <button type="submit" class="btn-icon-only" onclick="return confirm('Deseja realmente excluir esta categoria?')">
                                    <i class="fas fa-trash-alt btn-remover"></i>
                                </button>
                            </form>
                        </td>
                    `;
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

        fetch('/api/categorias', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ codigo, nome })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao adicionar categoria.');
            }
            return response.json();
        })
        .then(() => {
            carregarCategorias();
            limparFormulario();
        })
        .catch(error => {
            alert(error.message);
        });
    });

    function limparFormulario() {
        codigoInput.value = '';
        nomeInput.value = '';
    }

    btnLimpar.addEventListener('click', limparFormulario);

    // Função global para exclusão
    window.excluirCategoria = function (id) {
        fetch(`/api/categorias/${id}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao excluir categoria.');
            }
            return response.json();
        })
        .then(() => {
            carregarCategorias();
        })
        .catch(error => {
            alert(error.message);
        });

        return false; // impede o envio do formulário
    };

    carregarCategorias();
});
