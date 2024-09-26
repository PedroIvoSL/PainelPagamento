// Get the modal
var modal = document.getElementById("login-modal");

// Get the button that opens the modal
var btn = document.getElementById("consultar-btn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Format CNPJ (XX.XXX.XXX/XXXX-XX) on input
document.getElementById('cnpj').addEventListener('input', function (e) {
    let cnpj = e.target.value;

    // Remove any non-numeric characters
    cnpj = cnpj.replace(/\D/g, '');

    // Format as CNPJ (XX.XXX.XXX/XXXX-XX)
    cnpj = cnpj.replace(/^(\d{2})(\d)/, '$1.$2');
    cnpj = cnpj.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
    cnpj = cnpj.replace(/\.(\d{3})(\d)/, '.$1/$2');
    cnpj = cnpj.replace(/(\d{4})(\d)/, '$1-$2');

    e.target.value = cnpj;
});

// Format Valor (R$ XX.XXX,XX)
document.getElementById('valor').addEventListener('input', function (e) {
    let valor = e.target.value;

    // Remove non-numeric characters except commas and periods
    valor = valor.replace(/[^\d,]/g, '');

    // Format as currency (R$ XX.XXX,XX)
    valor = valor.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    valor = 'R$ ' + valor;

    e.target.value = valor;
});

document.querySelector('.payment-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent the form from submitting in the default way

    // Collect the form data
    const fornecedor = document.querySelector('input[name="fornecedor"]').value;
    const cnpj = document.querySelector('input[name="cnpj"]').value.replace(/\D/g, ''); // Remove formatting
    const valor = document.querySelector('input[name="valor"]').value.replace(/[^\d,]/g, ''); // Only get the number and comma
    const dataVencimento = document.querySelector('input[name="data_vencimento"]').value;
    const descricao = document.querySelector('textarea[name="descricao"]').value;
    const dadosPagamento = document.querySelector('input[name="dados_pgt"]').value;

    // Validate that important fields are not empty
    if (!fornecedor || !cnpj || !valor || !dataVencimento || !descricao || !dadosPagamento) {
        alert("Por favor, preencha todos os campos obrigatórios.");
        return; // Stop the function from continuing
    }

    // Optionally: Here you can send the form data via an API (like using fetch() or AJAX)
    console.log({
        fornecedor,
        cnpj,
        valor,
        dataVencimento,
        descricao,
        dadosPagamento
    });

    // Finally, submit the form after validation
    e.target.submit(); // This will now submit the form if everything is fine
});
