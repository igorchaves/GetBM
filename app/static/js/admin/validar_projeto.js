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
        mensagem.classList.add('d-none');
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
        mensagem.classList.add('d-none');

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
                mensagem.classList.remove('d-none');
                mensagem.classList.add('alert', 'erro', 'mostrar');
                return;
            }

            const botaoSalvar = this.querySelector('button[type="submit"]');
            botaoSalvar.disabled = true;

            const salvarResposta = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form)
            });

            if (salvarResposta.ok) {
                alert('Projeto cadastrado com sucesso!');
                window.location.href = urlProjetos;
            } else {
                throw new Error('Erro ao salvar projeto');
            }

        } catch (erro) {
            console.error('Erro ao verificar projeto:', erro);
            mensagem.textContent = 'Erro ao verificar projeto. Tente novamente.';
            mensagem.classList.remove('d-none');
            mensagem.classList.add('alert', 'erro', 'mostrar');
        }
    });

    // Redirecionamento ao cancelar (fora do submit)
    const btnCancelar = document.getElementById('btn-cancelar');
    if (btnCancelar) {
        btnCancelar.addEventListener('click', function () {
            window.location.href = urlProjetos;
        });
    }
});
