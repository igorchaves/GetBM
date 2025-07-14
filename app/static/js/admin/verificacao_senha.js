document.addEventListener('DOMContentLoaded', function () {
    const novaSenha = document.getElementById('novaSenha');
    const confirmarSenha = document.getElementById('confirmarSenha');

    const criterios = {
        maiuscula: { regex: /[A-Z]/, elemento: 'criterio-maiuscula' },
        minuscula: { regex: /[a-z]/, elemento: 'criterio-minuscula' },
        numero: { regex: /[0-9]/, elemento: 'criterio-numero' },
        especial: { regex: /[^A-Za-z0-9]/, elemento: 'criterio-especial' },
        comprimento: { regex: /.{8,}/, elemento: 'criterio-comprimento' }
    };

    function atualizarStatus(id, valido) {
        const el = document.getElementById(id);
        el.classList.remove('valido', 'invalido');
        el.classList.add(valido ? 'valido' : 'invalido');
    }

    function verificarSenha() {
        const senha = novaSenha.value;
        const confirmacao = confirmarSenha.value;

        for (const chave in criterios) {
            const { regex, elemento } = criterios[chave];
            atualizarStatus(elemento, regex.test(senha));
        }

        const iguais = senha && confirmacao && senha === confirmacao;
        atualizarStatus('criterio-igualdade', iguais);
    }

    novaSenha.addEventListener('input', verificarSenha);
    confirmarSenha.addEventListener('input', verificarSenha);
});
