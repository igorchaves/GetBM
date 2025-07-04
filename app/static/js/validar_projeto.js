document.getElementById('formProjeto').addEventListener('submit', async function (e) {
    e.preventDefault();

    const codigo = document.getElementById('codigoProjeto').value;
    const backlogs = Array.from(document.querySelectorAll('input[name="backlogs[]"]')).map(el => el.value.trim());
    const jornadas = Array.from(document.querySelectorAll('input[name="jornadas[]"]')).map(el => el.value.trim());
    const mensagem = document.getElementById('mensagemProjeto');



    console.log("Backlogs enviados:", backlogs);
    console.log("Jornadas enviadas:", jornadas);


    // Limpa mensagens anteriores
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


        // Desativa o botão para evitar duplo envio
        const botaoSalvar = this.querySelector('button[type="submit"]');
        botaoSalvar.disabled = true;

        this.submit();

    } catch (erro) {
        console.error('Erro ao verificar projeto:', erro);
        mensagem.textContent = 'Erro ao verificar projeto. Tente novamente.';
        mensagem.classList.add('alert', 'erro', 'mostrar');
    }

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

document.addEventListener("DOMContentLoaded", function () {
    setupTagInput('jornadaInput', 'jornadaLista', 'jornadas[]');
    setupTagInput('backlogInput', 'backlogLista', 'backlogs[]');
});