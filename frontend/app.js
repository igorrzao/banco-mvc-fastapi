const urlAPI = "http://127.0.0.1:8000";
let usuarioLogado = "";

async function buscarSaldo() {
    const nomeDigitado = document.getElementById("input-usuario").value;

    if (nomeDigitado === "") {
        alert("Digite o nome de usuário")
        return;
    }

    usuarioLogado = nomeDigitado;

    try {
        const resposta = await fetch(`${urlAPI}/saldo/${usuarioLogado}`);
        const dados = await resposta.json();
        const elementoSaldo = document.getElementById("saldo");
    

        if (dados.status === "erro") {
            elementoSaldo.innerText = "Usuário não encontrado";
            return;
        }
    
        elementoSaldo.innerText = `R$ ${dados.saldo.toFixed(2)}`;

    } catch (erro) {
        console.error("Erro ao conectar com a API:", erro);
        document.getElementById("saldo").innerText = "Erro na conexão";
    }
}

document.getElementById("btn-acessar").addEventListener("click", buscarSaldo);



async function realizarDeposito() {
    const inputValor = document.getElementById("valor");
    const valor = parseFloat(inputValor.value);

    if (isNaN(valor) || valor <= 0) {
        alert("Digite um valor válido para depósito.");
        return;
    }
    
    if (!usuarioLogado) {
        alert("Identifique-se primeiro digitando seu nome de usuário.");
        return;
    }

    try {
        const resposta = await fetch(`${urlAPI}/deposito/${usuarioLogado}/${valor}`, {
            method: "POST"
        });

        const dados = await resposta.json();

        if (dados.status === "sucesso") {
            document.getElementById("saldo").innerText = `R$ ${dados.novo_saldo.toFixed(2)}`;


            inputValor.value = "";

            alert("Depósito realizado com sucesso!");
        } else {
            alert(dados.motivo || "Erro ao realizar depósito.");
        }

    } catch (erro) {
        console.error("Erro no depósito:", erro);
        alert("Erro ao conectar com o servidor.");
    }
}

document.getElementById("btn-depositar").addEventListener("click", realizarDeposito);
    

async function realizarSaque() {
    const inputValor = document.getElementById("valor");
    const valor = parseFloat(inputValor.value);
    const senhaDigitada = document.getElementById("input-senha").value;

    if (isNaN(valor) || valor <= 0) {
        alert("Digite um valor válido para saque");
        return;
    }

    if (!usuarioLogado) {
        alert("Identifique-se primeiro digitando seu nome de usuário.");
        return;
    }

    try {
        const resposta = await fetch(`${urlAPI}/saque/${usuarioLogado}/${senhaDigitada}/${valor}`, {
            method: "POST"
        });

        const dados = await resposta.json();

        if (dados.status === "sucesso") {
            document.getElementById("saldo").innerText = `R$ ${dados.novo_saldo.toFixed(2)}`;

            inputValor.value = "";
            alert("Saque realizado com sucesso!");
        } else {
            alert(dados.motivo || "Erro ao realizar saque.");
        }
        
    } catch (erro) {
        console.error("Erro no saque:", erro);
        alert("Erro ao conectar com o servidor.");
    }
}

document.getElementById("btn-sacar").addEventListener("click", realizarSaque);