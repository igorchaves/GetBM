document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('form-sprint');
  const tabela = document.getElementById('tabela-sprints');
  const campoDataInicio = document.getElementById('data_inicio');

  // Define apenas o mínimo como hoje, mas não preenche o valor
  const hoje = new Date().toISOString().split('T')[0];
  campoDataInicio.setAttribute('min', hoje);

  carregarTabela();

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const sprint = document.getElementById('sprint').value.trim();
    const data_inicio = campoDataInicio.value;
    const duracao = document.getElementById('duracao').value;

    if (!sprint || !data_inicio || !duracao) {
      alert('Todos os campos são obrigatórios.');
      return;
    }

    try {
      const response = await fetch('/api/sprints', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sprint, data_inicio, duracao })
      });

      const result = await response.json();
      if (response.ok) {
        form.reset();
        campoDataInicio.setAttribute('min', hoje); // Reaplica restrição após reset
        carregarTabela();
      } else {
        alert(result.error || 'Erro ao cadastrar sprint.');
      }
    } catch (error) {
      alert('Erro de conexão com o servidor.');
    }
  });

  async function carregarTabela() {
    try {
      const response = await fetch('/api/sprints');
      const sprints = await response.json();

      tabela.innerHTML = '';

      if (sprints.length === 0) {
        tabela.innerHTML = '<tr><td colspan="4" class="text-center">Nenhuma sprint cadastrada.</td></tr>';
        return;
      }

      sprints.forEach(sprint => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${sprint.nome}</td>
          <td>${formatarData(sprint.data_inicio)}</td>
          <td>${formatarData(sprint.data_fim)}</td>
          <td>
            <form onsubmit="return excluirSprint(${sprint.id});" style="display:inline;">
              <button type="submit" class="btn-icon-only">
                <i class="fas fa-trash-alt btn-remover"></i>
              </button>
            </form>
          </td>
        `;
        tabela.appendChild(tr);
      });
    } catch (error) {
      tabela.innerHTML = '<tr><td colspan="4" class="text-center">Erro ao carregar sprints.</td></tr>';
    }
  }

  window.excluirSprint = async function(id) {
    if (!confirm('Deseja realmente excluir esta sprint?')) return false;

    try {
      const response = await fetch(`/api/sprints/${id}`, { method: 'DELETE' });
      const result = await response.json();
      if (response.ok) {
        carregarTabela();
      } else {
        alert(result.error || 'Erro ao excluir sprint.');
      }
    } catch (error) {
      alert('Erro de conexão com o servidor.');
    }

    return false;
  }

  function formatarData(dataISO) {
    const [ano, mes, dia] = dataISO.split('-');
    return `${dia}/${mes}/${ano}`;
  }
});
