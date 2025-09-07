// Aguarda o documento HTML ser totalmente carregado
document.addEventListener('DOMContentLoaded', function() {
    // Seleciona o formulário de cadastro de produtos
    const formCadastro = document.querySelector('form');

    // Adiciona um "ouvinte" para o evento de envio do formulário
    formCadastro.addEventListener('submit', function(event) {
        // Seleciona os campos do formulário
        const nome = document.querySelector('input[name="nome"]').value;
        const preco = document.querySelector('input[name="preco"]').value;
        const quantidade = document.querySelector('input[name="quantidade"]').value;

        // Verifica se algum campo está vazio
        if (nome.trim() === '' || preco.trim() === '' || quantidade.trim() === '') {
            // Se estiver, impede o envio do formulário
            event.preventDefault(); 
            // Mostra uma mensagem de alerta
            alert('Por favor, preencha todos os campos obrigatórios.');
        }
    });
});