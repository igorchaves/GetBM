document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('formProjeto');
    const mensagem = document.getElementById('mensagemProjeto');

    // Configura inputs de tags
    setupTagInput('jornadaInput', 'jornadaLista', 'jornadas[]');
    setupTagInput('backlogInput', 'backlogLista', 'backlogs[]');

    // Limpa mensagens e listas ao resetar o formulário
    form.addEventListener('reset', function () {
        mensagem.textContent = '';
        mensagem.classList.remove('mostrar', 'erro', 'alert');
        document.getElementById('backlogLista').innerHTML = '';
        document.getElementById('jornadaLista').innerHTML = '';
    });

    // Validação e envio do formulário
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const codigo = document.getElementById('codigoProjeto').value;
        const backlogs = Array.from(document.querySelectorAll('input[name="backlogs[]"]')).map(el => el.value.trim());
        const jornadas = Array.from(document.querySelectorAll('input[name="jornadas[]"]')).map(el => el.value.trim());

        mensagem.textContent = '';
        mensagem.classList.remove('mostrar', 'erro', 'alert');

        try {
            const resposta = await fetch('/verificar-projeto', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    codigoProjeto: codigo,
                    backlogs: backlogs,
                    jornadas: jornadas
                })
            });

            const resultado = await resposta.json();

            if (resultado.existe) {
                mensagem.textContent = resultado.mensagem;
                mensagem.classList.add('alert', 'erro', 'mostrar');
                return;
            }

            const botaoSalvar = this.querySelector('button[type="submit"]');
            botaoSalvar.disabled = true;
            this.submit();

        } catch (erro) {
            console.error('Erro ao verificar projeto:', erro);
            mensagem.textContent = 'Erro ao verificar projeto. Tente novamente.';
            mensagem.classList.add('alert', 'erro', 'mostrar');
        }
    });
});

function setupTagInput(inputId, listId, inputName) {
    const input = document.getElementById(inputId);
    const list = document.getElementById(listId);

    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && input.value.trim() !== '') {
            e.preventDefault();
            const valor = input.value.trim();

            const li = document.createElement('li');
            li.className = 'tag-item';
            li.innerHTML = `
                <span>${valor}</span>
                <button type="button" class="remove-btn" onclick="this.parentElement.remove()">×</button>
                <input type="hidden" name="${inputName}" value="${valor}">
            `;
            list.appendChild(li);
            input.value = '';
        }
    });
}
