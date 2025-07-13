document.getElementById('login-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const usuario = this.usuario.value;
    const senha = this.senha.value;

    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ usuario, senha })
        });

        const data = await response.json();

        if (response.ok) {
            // O token já está no cookie, redireciona para a rota protegida
            window.location.href = '/home';
        } else {
            alert(data.erro || 'Erro ao fazer login');
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        alert('Erro ao conectar com o servidor.');
    }
});
