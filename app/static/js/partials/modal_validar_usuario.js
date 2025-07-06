document.getElementById('formUsuario').addEventListener('submit', async function (e) {
    e.preventDefault();

    const codigo = document.getElementById('codigoUsuario').value;
    const mensagem = document.getElementById('mensagemUsuario');

    // Limpa mensagem anterior
    mensagem.textContent = '';
    mensagem.classList.remove('mostrar', 'erro', 'alert');

    try {
        const resposta = await fetch('/verificar-usuario', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codigoUsuario: codigo })
        });

        const resultado = await resposta.json();
        console.log(resultado);

        if (resultado.existe) {
            mensagem.textContent = resultado.mensagem;
            mensagem.classList.add('alert', 'erro', 'mostrar');
            return;
        }

        this.submit();

    } catch (erro) {
        console.error('Erro ao verificar usuário:', erro);
        mensagem.textContent = 'Erro ao verificar usuário. Tente novamente.';
        mensagem.classList.add('alert', 'erro', 'mostrar');
    }
});


// ✅ Função para limpar o formulário e a mensagem
function limparFormularioUsuario() {
  const form = document.getElementById('formUsuario');
  const mensagem = document.getElementById('mensagemUsuario');

  form.reset(); // limpa os campos
  mensagem.textContent = '';
  mensagem.classList.remove('mostrar', 'erro', 'alert');
}

// Botão "Cancelar"
const btnCancelar = document.querySelector('.modal-btn-cancelar');
if (btnCancelar) {
  btnCancelar.addEventListener('click', () => {
    limparFormularioUsuario();
    document.getElementById('modalUsuario').style.display = 'none';
  });
}

// Botão "Fechar (X)"
const btnFechar = document.querySelector('.close');
if (btnFechar) {
  btnFechar.addEventListener('click', () => {
    limparFormularioUsuario();
    document.getElementById('modalUsuario').style.display = 'none';
  });
}
