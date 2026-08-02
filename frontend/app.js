const urlAPI = "http://127.0.0.1:8000";
let usuarioLogado = "";
let token = "";



async function fazerLogin() {

    const usuarioDigitado = document.getElementById("input-usuario").value;
    const senhaDigitada = document.getElementById("input-senha").value;

    if (!usuarioDigitado || !senhaDigitada) {
        alert("Preencha com um usuário e senha.");
        return;
    }

    try {
        const resposta = await fetch(`${urlAPI}/login`, {
        method: "POST", headers: { "Content-Type": "application/json"},
        body:JSON.stringify({
            usuario: usuarioDigitado,
            senha: senhaDigitada
            })
        });
    
        const resultado = await resposta.json();

        if (resultado.status === "sucesso") {
            usuarioLogado = usuarioDigitado;
            alert("Login realizado com sucesso.");
            buscarSaldo();
        } else {
            alert(resultado.motivo || "Usuário ou senha incorretos.");
        }
    } catch (erro) {
        console.error("Erro no login:", erro);
            alert("Erro ao conectar ao servidor.");
    }
}    

document.getElementById("btn-acessar").addEventListener("click", fazerLogin);



async function buscarSaldo() {
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





async function realizarDeposito() {
    const inputValor = document.getElementById("valor");
    const valor = parseFloat(inputValor.value);

    if (isNaN(valor) || valor <= 0) {
        alert("Digite um valor válido para depósito.");
        return;
    }
    
    if (!usuarioLogado) {
        alert("Identifique-se primeiro realizando login.");
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











