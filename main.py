from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import inicializar_banco
from repository import verificar_credenciais, atualizar_saldo, buscar_saldo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

inicializar_banco()



@app.get("/saldo/{nome_usuario}")
def verificar_saldo(nome_usuario:str):
    resposta = buscar_saldo(nome_usuario)

    if resposta["status"] == "erro":
        return resposta
    
    return resposta
    

@app.post("/deposito/{nome_usuario}/{valor}")
def depositar(nome_usuario:str, valor:float):

    if valor <= 0:
        return{"status":"erro", "motivo": "Valor inserido inválido para depósito."}


    resposta = buscar_saldo(nome_usuario)

    if resposta["status"] == "erro":
        return resposta
    
    saldo_atual = resposta["saldo"]

    novo_saldo = saldo_atual + valor
    atualizar_saldo(nome_usuario, novo_saldo)
    
    return {
        "status": "sucesso",
        "mensagem": "Depósito realizado com sucesso!",
        "titular": nome_usuario,
        "saldo_anterior": saldo_atual,
        "novo_saldo": novo_saldo
    }


@app.post("/saque/{nome_usuario}/{senha}/{valor}")
def sacar(nome_usuario:str, senha:str, valor:float):

    if valor <= 0:
        return{"status":"erro", "motivo": "O valor do saque deve ser maior que zero."}

    resposta = verificar_credenciais(nome_usuario, senha)

    if resposta["status"] == "erro":
        return resposta
    
    saldo_atual = resposta["saldo"]
    

    if saldo_atual >= valor:
        novo_saldo = saldo_atual - valor

        atualizar_saldo(nome_usuario, novo_saldo)

        return {
            "status": "sucesso",
            "mensagem": "Saque realizado com sucesso!",
            "titular": nome_usuario,
            "saldo_anterior": saldo_atual,
            "novo_saldo": novo_saldo
        }
    
    else:
        return{"status":"erro", "motivo": "Saldo insuficiente."}
    

@app.post("/transferir/{nome_usuario}/{senha}/{valor}/{usuario_alvo}")
def transferir(nome_usuario:str, senha:str, valor:float, usuario_alvo:str):

    if valor <= 0:
        return{"status":"erro", "motivo": "O valor para transferência deve ser maior que zero."}
    if nome_usuario == usuario_alvo:
        return{"status":"erro", "motivo": "O remetente não pode ser igual ao destinatário."}

    resposta = verificar_credenciais(nome_usuario, senha)

    if resposta["status"] == "erro":
        return resposta
    
    saldo_remetente = resposta["saldo"]

    resposta2 = buscar_saldo(usuario_alvo)

    if resposta2["status"] == "erro" and resposta2["motivo"] == "Usuário não encontrado.":
        return{"status":"erro", "motivo":"O usuário de destino não foi encontrado."}
    
    saldo_destinatario = resposta2["saldo"]

    
    if saldo_remetente >= valor:
        saldo_destinatario += valor
        novo_saldo_remetente = saldo_remetente - valor

        atualizar_saldo(nome_usuario, novo_saldo_remetente)
        atualizar_saldo(usuario_alvo, saldo_destinatario)

        return {
            "status": "sucesso",
            "mensagem": "Transferência realizada com sucesso!",
            "remetente": nome_usuario,
            "destinatário": usuario_alvo,
            "novo_saldo_remetente": novo_saldo_remetente,
            "novo_saldo_destinatario": saldo_destinatario
        }
    
    else:
        return{"status":"erro", "motivo":"Saldo insuficiente."}