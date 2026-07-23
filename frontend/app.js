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