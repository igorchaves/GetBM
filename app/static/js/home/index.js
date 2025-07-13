// A verificação do token no sessionStorage foi removida
// O cookie com o token será enviado automaticamente pelo navegador

/*fetch('/api/dados-home')
  .then(res => {
    if (!res.ok) {
      throw new Error('Falha ao carregar dados');
    }
    return res.json();
  })
  .then(data => {
    // renderiza dados na tela
    console.log('Dados recebidos:', data);
  })
  .catch(err => {
    console.error('Erro ao carregar dados:', err);
    window.location.href = '/auth/login';
  });
*/


  // Nenhuma verificação de token é necessária aqui
// O backend já protege a rota /home com @login_requerido

// Se quiser adicionar interações JS, pode fazer aqui
console.log('Página /home carregada com sucesso');
