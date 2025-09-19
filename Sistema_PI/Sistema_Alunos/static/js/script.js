function buscarAluno() {
    const termoBusca = document.getElementById("busca").value;
    // A busca real será implementada no backend
    alert(`Buscando por: ${termoBusca}`);
}

const cadastroForm = document.getElementById("cadastro-form");
if (cadastroForm) { // Verifica se o formulário existe na página
    cadastroForm.addEventListener("submit", function(event) {
        event.preventDefault();
        // O envio para o backend será implementado posteriormente
        alert("Aluno cadastrado (funcionalidade de envio para o backend será adicionada)");
    });
}